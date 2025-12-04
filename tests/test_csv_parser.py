import unittest
from app.routers.upload_csv import parse_csv_content

class TestCSVParser(unittest.TestCase):
    
    def test_parse_csv_content(self):
        csv_content = """date,employee_id,event_type,value,notes
2024-01-01,1,delivery_success,10.0,Delivered on time
2024-01-02,2,customer_rating,4.5,Good service
2024-01-03,1,presence,1.0,Present"""
        
        result = parse_csv_content(csv_content)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['employee_id'], 1)
        self.assertEqual(result[0]['type'], 'delivery_success')
        self.assertEqual(result[0]['value'], 10.0)
        self.assertEqual(result[1]['employee_id'], 2)
        self.assertEqual(result[2]['type'], 'presence')
    
    def test_parse_csv_with_missing_notes(self):
        csv_content = """date,employee_id,event_type,value
2024-01-01,1,delivery_success,10.0"""
        
        result = parse_csv_content(csv_content)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['notes'], '')

if __name__ == '__main__':
    unittest.main()