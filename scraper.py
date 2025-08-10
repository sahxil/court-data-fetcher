from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import uuid
import time
import requests

# --- Browser Configuration ---
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

def sanitize_html(html):
    if not html: return ""
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup.find_all("script"): script.decompose()
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr.startswith("on"): del tag.attrs[attr]
    return str(soup)


def start_session_and_get_captcha():
    """
    Starts a Selenium session by navigating directly to the case number form,
    downloads the CAPTCHA, and returns the driver and image path.
    """
    driver = webdriver.Chrome(options=chrome_options)
    # Direct navigation to the form page
    driver.get("https://www.allahabadhighcourt.in/apps/status_ccms/index.php/case-number")
    try:
        # We no longer need to click a link or switch tabs
        captcha_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captcha"))
        )
        captcha_url = captcha_element.get_attribute('src')
        cookies = driver.get_cookies()
        req_session = requests.Session()
        for cookie in cookies:
            req_session.cookies.set(cookie['name'], cookie['value'])
        response = req_session.get(captcha_url)
        if response.status_code == 200:
            captcha_filename = f"captcha_{uuid.uuid4()}.png"
            full_save_path = f"static/{captcha_filename}"
            with open(full_save_path, 'wb') as file:
                file.write(response.content)
            return {"status": "success", "driver": driver, "captcha_image_path": captcha_filename}
        else:
            raise Exception("Failed to download CAPTCHA image.")
    except Exception as e:
        driver.quit()
        return {"status": "error", "message": f"Failed to start session: {e}"}
    


def fetch_case_types():
    """
    Scrapes the list of available case types from the dropdown menu.
    """
    url = "https://www.allahabadhighcourt.in/apps/status_ccms/index.php/case-number"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        case_type_select = soup.find('select', {'id': 'case_type'})
        if not case_type_select:
            return []
            
        case_types = []
        for option in case_type_select.find_all('option'):
            if option.get('value'): # Ensure there is a value
                case_types.append({
                    'value': option.get('value'),
                    'text': option.text.strip()
                })
        return case_types
    except Exception as e:
        print(f"Error fetching case types: {e}")
        return [] # Return empty list on failure
    



def fill_form_and_get_results(driver, case_type, case_no, year, captcha_text):
    """
    Fills form, correctly handles success vs. error states, and scrapes the content.
    """
    try:
        Select(driver.find_element(By.ID, "case_type")).select_by_value(case_type)
        driver.find_element(By.ID, "case_no").send_keys(case_no)
        driver.find_element(By.ID, "case_year").send_keys(year)
        driver.find_element(By.ID, "captchacode").send_keys(captcha_text)
        driver.find_element(By.ID, "go_btn").click()

        # Wait for the page to respond with either a success table or an error message
        WebDriverWait(driver, 10).until(
            EC.any_of(
                EC.presence_of_element_located((By.CLASS_NAME, "table-info")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "#CaseInfoData .text-danger"))
            )
        )
        
        # --- THIS IS THE CORRECTED LOGIC ---
        try:
            # FIRST, try to find the success element.
            summary_table = driver.find_element(By.CLASS_NAME, "table-info")
            
            # If the above line succeeds, we know it was a successful search.
            # Now we proceed with the rest of the scraping steps.
            view_link = WebDriverWait(summary_table, 10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "view"))
            )
            driver.execute_script("arguments[0].click();", view_link)
            
            print_panel_div = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "printpanel"))
            )
            
            main_content_html = print_panel_div.get_attribute('innerHTML')
            history_html = ""
            order_html = ""

            try:
                history_button = driver.find_element(By.CSS_SELECTOR, 'button[data-target="#casehistory"]')
                driver.execute_script("arguments[0].click();", history_button)
                history_content_div = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "#casehistory"))
                )
                history_html = history_content_div.get_attribute('innerHTML')
            except Exception as e:
                print(f"Could not get Listing History content: {e}")

            try:
                order_button = driver.find_element(By.CSS_SELECTOR, 'button[data-target="#judgementorder"]')
                driver.execute_script("arguments[0].click();", order_button)
                order_content_div = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#viewOrderDiv table"))
                )
                order_html = order_content_div.get_attribute('innerHTML')
            except Exception as e:
                print(f"Could not get Judgement/Order content: {e}")
            
            soup = BeautifulSoup(main_content_html, 'html.parser')
            for button in soup.find_all('button', {'data-toggle': 'collapse'}):
                button.decompose()
            cleaned_main_content_html = str(soup)

            return {
                "status": "success",
                "main_content_html": sanitize_html(cleaned_main_content_html),
                "history_html": sanitize_html(history_html),
                "order_html": sanitize_html(order_html),
                "raw_html": driver.page_source
            }

        except:
            # If we CAN'T find the success table, THEN it must be an error.
            error_element = driver.find_element(By.CSS_SELECTOR, "#CaseInfoData .text-danger")
            return {"status": "error", "message": error_element.text, "raw_html": driver.page_source}

    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred during search: {e}"}
    finally:
        driver.quit()
