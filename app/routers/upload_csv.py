from fastapi import APIRouter, UploadFile, File, HTTPException
from app.database import get_db
from app.schemas import CSVUploadResponse
import csv
import io

router = APIRouter()

def parse_csv_content(content: str) -> list:
    """Parse CSV content and return list of rows"""
    content = content.strip()
    reader = csv.DictReader(io.StringIO(content))
    rows = []
    
    # Check if required columns exist
    fieldnames = reader.fieldnames
    if not fieldnames:
        raise ValueError("CSV file is empty or has no headers")
    
    required_cols = ['date', 'employee_id', 'event_type', 'value']
    missing_cols = [col for col in required_cols if col not in fieldnames]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    for row in reader:
        if not any(row.values()):  # Skip empty rows
            continue
        
        employee_id_raw = row['employee_id'].strip()
        # Extract employee code and name if format is "CODE - Name"
        if ' - ' in employee_id_raw:
            emp_code, emp_name = employee_id_raw.split(' - ', 1)
        else:
            emp_code = employee_id_raw
            emp_name = employee_id_raw
        
        # Convert date format from M/D/YYYY to YYYY-MM-DD
        date_str = row['date'].strip()
        if '/' in date_str:
            date_parts = date_str.split('/')
            if len(date_parts) == 3:
                month, day, year = date_parts
                formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            else:
                formatted_date = date_str
        else:
            formatted_date = date_str
        
        rows.append({
            'date': formatted_date,
            'employee_code': emp_code.strip(),
            'employee_name': emp_name.strip(),
            'type': row['event_type'].strip(),
            'value': float(row['value']),
            'notes': row.get('notes', '').strip()
        })
    return rows

@router.post("/upload-csv", response_model=CSVUploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")
    
    try:
        content = await file.read()
        content_str = content.decode('utf-8-sig')  # Handle BOM
        
        rows = parse_csv_content(content_str)
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Process each row and create employees if needed
            for row in rows:
                # Get or create employee
                cursor.execute("SELECT id FROM employees WHERE role = ?", (row['employee_code'],))
                employee = cursor.fetchone()
                
                if not employee:
                    cursor.execute("""
                        INSERT INTO employees (name, role, branch)
                        VALUES (?, ?, ?)
                    """, (row['employee_name'], row['employee_code'], 'Driver'))
                    employee_id = cursor.lastrowid
                else:
                    employee_id = employee[0]
                
                # Insert event
                cursor.execute("""
                    INSERT INTO events (employee_id, date, type, value, notes)
                    VALUES (?, ?, ?, ?, ?)
                """, (employee_id, row['date'], row['type'], row['value'], row['notes']))
            
            conn.commit()
        
        return CSVUploadResponse(
            rows_inserted=len(rows),
            message=f"Successfully inserted {len(rows)} events"
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")