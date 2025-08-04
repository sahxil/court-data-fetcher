# Court-Data Fetcher & Mini-Dashboard

This web application is a submission for an internship task. It allows users to fetch case data from the Allahabad High Court's public portal.

---

### Court Chosen

As per the task requirements, a specific court had to be chosen for scraping.

- **Court:** High Court of Judicature at Allahabad
- **URL:** `https://www.allahabadhighcourt.in/apps/status_ccms/`

---

### Setup and Run Instructions

To run this project locally, please follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone <Your-Repo-URL>
    cd <repository-folder>
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    (This only needs to be run once to create the `queries.db` file)

    ```bash
    python database.py
    ```

5.  **Run the Flask application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

---

### CAPTCHA Strategy

The target website is protected by an image-based CAPTCHA that cannot be solved programmatically without external services. [cite_start]To circumvent this legally and creatively, this project uses a "human-in-the-loop" or "manual token" approach[cite: 29].

**Workflow:**

1.  When the user loads the homepage, the Flask backend initiates a live Selenium session with the court's website.
2.  The scraper navigates to the search form and downloads the exact CAPTCHA image presented in that specific session.
3.  This session-specific image is then displayed to the user in the web app's frontend.
4.  The user manually types the characters from the image. This input is then sent back to the backend.
5.  The scraper uses the user's input to complete the form within the original live session and submit the request.

This method is robust, legal, and effectively handles the CAPTCHA challenge without relying on third-party APIs.

---

### Environment Variables

This application is self-contained and does not require any external API keys or secret environment variables to run.
