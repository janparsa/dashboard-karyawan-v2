import sqlite3
from contextlib import contextmanager

DATABASE_URL = "db.sqlite3"

def init_db():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            role TEXT,
            branch TEXT
        )
    """)
    
    # Create events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            date TEXT,
            type TEXT,
            value REAL,
            notes TEXT,
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    """)
    
    # Create scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            period_start TEXT,
            period_end TEXT,
            score_json TEXT
        )
    """)
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()