import unittest
import sqlite3
import tempfile
import os
from app.scoring import calculate_score

class TestScoring(unittest.TestCase):
    
    def setUp(self):
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Override database path
        import app.database
        app.database.DATABASE_URL = self.db_path
        
        # Initialize test database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                role TEXT,
                branch TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE events (
                id INTEGER PRIMARY KEY,
                employee_id INTEGER,
                date TEXT,
                type TEXT,
                value REAL,
                notes TEXT
            )
        """)
        
        # Insert test data
        cursor.execute("INSERT INTO employees VALUES (1, 'Test Employee', 'Driver', 'Jakarta')")
        
        # Insert test events
        test_events = [
            (1, '2024-01-01', 'delivery_success', 10.0, ''),
            (1, '2024-01-02', 'customer_rating', 4.5, ''),
            (1, '2024-01-03', 'presence', 1.0, ''),
            (1, '2024-01-04', 'complaint', 1.0, ''),
        ]
        
        for event in test_events:
            cursor.execute("""
                INSERT INTO events (employee_id, date, type, value, notes)
                VALUES (?, ?, ?, ?, ?)
            """, event)
        
        conn.commit()
        conn.close()
    
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_calculate_score(self):
        result = calculate_score(1, '2024-01-01', '2024-01-31')
        
        self.assertIsInstance(result, dict)
        self.assertIn('score_total', result)
        self.assertIn('details', result)
        self.assertGreaterEqual(result['score_total'], 0)
        self.assertLessEqual(result['score_total'], 100)

if __name__ == '__main__':
    unittest.main()