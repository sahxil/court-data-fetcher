# Court-Data Fetcher & Mini-Dashboard ⚖️

A full-stack Python web application that automates fetching and displaying real-time case data from the Allahabad High Court's public portal. This project demonstrates robust web scraping, a clean user interface, and resilient error handling.

**[▶️ Watch the Demo Video](https://drive.google.com/file/d/1NyQ01wsOag2o3BLSxoCd7gr9R-p_ePrZ/view?usp=drive_link)**

---

## Features ✨

-   **🖥️ Simple & Clean UI**: A straightforward web form for case data submission.
-   **🤖 Robust Selenium Scraper**: Navigates the court's complex, multi-page, JavaScript-driven website.
-   **🔒 Legal CAPTCHA Handling**: Implements a "human-in-the-loop" strategy to legally and effectively bypass the image CAPTCHA.
-   **🔄 Dynamic Content Loading**: The list of "Case Types" is scraped in real-time to ensure it's always up-to-date.
-   **✅ Intelligent Error Handling**: Provides specific user-friendly messages for "Record Not Found" and "Incorrect CAPTCHA" errors.
-   **🗄️ Database Logging**: Every query and its raw HTML response is logged to an SQLite database for auditing.
-   **📄 Stable Results Page**: Uses a Post/Redirect/Get pattern to prevent annoying "Confirm Form Resubmission" warnings on refresh.
-   **✨ Polished Presentation**: The final results are displayed in a clean, self-contained Bootstrap accordion, completely decoupled from the source site's messy frontend code.

## Architecture 🏗️
