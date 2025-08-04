import sqlite3
import datetime

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect('queries.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the logs table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            case_type TEXT NOT NULL,
            case_number TEXT NOT NULL,
            year TEXT NOT NULL,
            status TEXT NOT NULL,
            raw_response_html TEXT
        );
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def log_query(case_type, case_number, year, status, raw_response_html=""):
    """Logs a query attempt to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO logs (timestamp, case_type, case_number, year, status, raw_response_html) VALUES (?, ?, ?, ?, ?, ?)",
        (timestamp, case_type, case_number, year, status, raw_response_html)
    )
    conn.commit()
    conn.close()

# This part allows you to run `python database.py` from the terminal to set up the DB.
if __name__ == '__main__':
    init_db()