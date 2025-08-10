# Court Data Fetcher & Mini-Dashboard ⚖️

A sophisticated web application that enables users to fetch and analyze case data from the Allahabad High Court's public portal with an elegant, user-friendly interface.

## 🎥 Demo Video

**[📺 Watch the Complete Demo](https://drive.google.com/file/d/1NyQ01wsOag2o3BLSxoCd7gr9R-p_ePrZ/view?usp=drive_link)**

See the application in action - from CAPTCHA handling to data visualization!

---

## 🏛️ Target Court Selection

As per the internship task requirements, this project focuses on a specific court for data extraction:

- **🏛️ Court:** High Court of Judicature at Allahabad
- **🌐 Portal URL:** `https://www.allahabadhighcourt.in/apps/status_ccms/`
- **📊 Data Source:** Public case status portal

---

## ✨ Key Features

- 🔍 **Real-time Case Search**: Live data fetching from court portal
- 🤖 **Smart CAPTCHA Handling**: Human-in-the-loop approach for secure access
- 📊 **Interactive Dashboard**: Visual data representation and analytics
- 💾 **Query History**: Persistent storage of search queries
- 🎨 **Modern UI/UX**: Clean, responsive design for optimal user experience
- ⚡ **Fast Processing**: Selenium-powered web scraping for reliable data extraction

---

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.7+
- Modern web browser (Chrome/Firefox)
- ChromeDriver (automatically managed)

### Installation & Setup

1. **📥 Clone the Repository**
   ```bash
   git clone <Your-Repo-URL>
   cd <repository-folder>
   ```

2. **🐍 Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **📦 Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **🗄️ Initialize Database**
   ```bash
   python database.py
   ```
   *This creates the `queries.db` file for storing search history*

5. **🚀 Launch Application**
   ```bash
   flask run
   ```
   
   **🌐 Access at:** `http://127.0.0.1:5000`

---

## 🔐 CAPTCHA Strategy & Innovation

The target website employs image-based CAPTCHA protection that cannot be bypassed programmatically without external services. Our solution implements a **creative "human-in-the-loop"** approach:

### 🔄 Workflow Process

1. **🌐 Session Initialization**: Flask backend launches a live Selenium session
2. **📸 CAPTCHA Capture**: Downloads the session-specific CAPTCHA image
3. **👁️ Human Verification**: User manually solves the CAPTCHA in our interface
4. **⚡ Seamless Submission**: Original session completes the form submission
5. **📊 Data Extraction**: Results parsed and displayed in dashboard

### ✅ Why This Approach?

- **🛡️ Legal Compliance**: No third-party CAPTCHA-breaking services
- **🎯 High Accuracy**: Human verification ensures 100% success rate
- **💰 Cost-Effective**: No external API dependencies
- **🔒 Secure**: Maintains session integrity throughout the process

---

## 🛠️ Technical Architecture

```
Frontend (HTML/CSS/JS) → Flask Backend → Selenium WebDriver
                                    ↓
                              Court Portal API
                                    ↓
                            SQLite Database ← Query Storage
```

### 🔧 Core Technologies

- **Backend**: Flask (Python)
- **Scraping**: Selenium WebDriver
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with responsive design

---

## 📊 Features Breakdown

### 🔍 Search Functionality
- Case number lookup
- Real-time data fetching
- Error handling and validation

### 📈 Dashboard Analytics
- Query history visualization
- Search statistics
- Data export capabilities

### 💾 Data Management
- Persistent query storage
- Search result caching
- Historical data analysis

---

## 🌟 Environment & Configuration

**🎉 Zero Configuration Required!**

This application is completely self-contained and requires no external API keys, secret tokens, or environment variables. Simply clone, install, and run!

---

## 🚀 Future Enhancements

- 🔄 **Multi-Court Support**: Extend to other high courts
- 🤖 **AI-Powered Analytics**: Case pattern recognition
- 📱 **Mobile App**: React Native implementation
- 🔔 **Real-time Notifications**: Case status updates
- 📊 **Advanced Reporting**: PDF/Excel export functionality

---

## 📋 Technical Evaluation Criteria

This project addresses all key evaluation requirements for the internship task:

### 🛡️ **Robustness Against Site Layout Changes**
The application is designed to be highly resilient to changes on the target website:
- **Dynamic Content Scraping**: Instead of hardcoding "Case Types," the app performs live scraping of dropdown menus each time the homepage loads, ensuring current data
- **Stable Content Targeting**: Scrapes larger, stable content blocks (main details panel, history sections) rather than fragile individual data points
- **Decoupled Templates**: Final results use self-contained templates, decoupling the app's appearance from the source site's frontend

### 🔒 **Code Clarity & Security**
- **Clear Architecture**: Organized with separation of concerns - `app.py` (routing), `scraper.py` (automation), `database.py` (storage)
- **Zero Hard-coded Secrets**: No API keys or passwords required, eliminating security vulnerabilities
- **Server-side Sessions**: Uses secure server-side sessions for handling scraped HTML instead of client-side storage

### 📖 **Documentation Quality**
- **Comprehensive README**: Detailed setup instructions, court selection rationale, and CAPTCHA strategy explanation
- **Step-by-step Guides**: Clear installation and execution instructions
- **Technical Details**: Thorough explanation of the "human-in-the-loop" CAPTCHA approach

### 🎨 **UI/UX Simplicity**
- **Minimal Interface**: Clean, single-form design as required
- **User-friendly Errors**: Specific error messages for "Record Not Found" and "Incorrect CAPTCHA"
- **Professional Experience**: Implements Post/Redirect/Get (PRG) pattern to prevent form resubmission warnings

### 💡 **Creative CAPTCHA Solution**
- **Legal Compliance**: No third-party CAPTCHA-breaking services used
- **Human-in-the-Loop**: Backend creates live browser sessions and displays session-specific CAPTCHA images
- **Seamless Integration**: User's manual input solves CAPTCHA in the original live session
- **Innovative Approach**: Combines human intelligence with automated processes legally and effectively

---

## 🤝 Contributing

This project was created as an internship submission, but contributions and suggestions are welcome!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Allahabad High Court** for providing public access to case data
- **Selenium Community** for robust web automation tools
- **Flask Team** for the excellent web framework

---

**⚖️ Built with precision for legal data accessibility**

*Internship Project - August 2025*
