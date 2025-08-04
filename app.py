from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from scraper import start_session_and_get_captcha, fill_form_and_get_results, fetch_case_types
from database import log_query
import uuid
import atexit

app = Flask(__name__)

# --- CONFIGURATION FOR SERVER-SIDE SESSIONS ---
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# ---------------------------------------------------

active_drivers = {}

@app.route('/')
def index():
    """
    Renders the main search page. It dynamically fetches the latest case types
    and starts a new scraper session to get a CAPTCHA image.
    """
    session.pop('result_data', None) # Clear any old result data

    # First, fetch the dynamic list of case types for robustness
    case_types = fetch_case_types()
    if not case_types:
        return render_template('error.html', message="Could not fetch the list of case types from the court website. The site may be down or has changed.")

    # Then, start the session for the CAPTCHA
    session_id = str(uuid.uuid4())
    result = start_session_and_get_captcha()
    if result.get('status') == 'error':
        return render_template('error.html', message=result.get('message', 'An unknown error occurred.'))
    
    active_drivers[session_id] = result['driver']
    session['session_id'] = session_id
    
    # Pass the dynamic list of case types to the template
    return render_template(
        'index.html', 
        captcha_image=result.get('captcha_image_path'),
        case_types=case_types
    )

@app.route('/search', methods=['POST'])
def search():
    """
    Handles the form submission, triggers the scraper, logs the attempt,
    and redirects to the results page on success.
    """
    session_id = session.get('session_id')
    driver = active_drivers.pop(session_id, None)
    if not driver:
        return render_template('error.html', message="Your session expired. Please try again.")
    
    case_type = request.form['case_type']
    case_no = request.form['case_no']
    year = request.form['year']
    captcha_text = request.form['captcha_text']
    
    result = fill_form_and_get_results(driver, case_type, case_no, year, captcha_text)
    
    log_query(case_type, case_no, year, result.get('status'), result.get('raw_html', ''))
    
    if result.get('status') == 'success':
        # Store the successfully scraped and sanitized content in the session
        session['result_data'] = {
            'main_content': result.get('main_content_html', ''),
            'history': result.get('history_html', ''),
            'order': result.get('order_html', '')
        }
        return redirect(url_for('show_results'))
    else:
        # If the scraper returned an error, show the error page
        return render_template('error.html', message=result.get('message', 'An unknown error occurred.'))

@app.route('/results')
def show_results():
    """
    Displays the results from the session using a clean, self-contained template.
    This is a GET route to prevent form resubmission warnings on refresh.
    """
    result_data = session.get('result_data')
    if not result_data:
        # If there's no data (e.g., user navigates here directly), go home
        return redirect(url_for('index'))
        
    return render_template(
        'results.html', 
        main_content=result_data.get('main_content'),
        history_content=result_data.get('history'),
        order_content=result_data.get('order')
    )

@atexit.register
def close_all_drivers():
    """
    Ensures all leftover Selenium browser instances are closed when the app shuts down.
    """
    for driver in active_drivers.values():
        driver.quit()
    print("All active drivers have been closed.")

if __name__ == '__main__':
    app.run(debug=True)