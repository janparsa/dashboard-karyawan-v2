# Scoreboard Produktivitas SDM

A complete MVP system for tracking and scoring employee productivity in expedition/logistics business.

## Features

- FastAPI backend with SQLite database
- CSV data upload functionality
- Configurable scoring engine with weighted metrics
- REST API for employee scores
- Static HTML dashboard with Bootstrap UI
- Docker containerization

## Project Structure

```
app/
├── main.py              # FastAPI application
├── models.py            # Pydantic models
├── database.py          # SQLite database setup
├── schemas.py           # API response schemas
├── scoring.py           # Scoring engine
├── config/
│   └── scoring_config.json  # Scoring weights
├── routers/
│   ├── upload_csv.py    # CSV upload endpoint
│   └── scores.py        # Scores API endpoint
└── static/
    └── index.html       # Dashboard UI
tests/
├── test_scoring.py      # Scoring engine tests
└── test_csv_parser.py   # CSV parser tests
```

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload --port 8002
```

3. Open browser to `http://localhost:8002`

## Running with Docker

1. Build and run with docker-compose:
```bash
docker-compose up --build
```

2. Access at `http://localhost:8002`

## API Documentation

### Health Check
- `GET /health` - Returns system status

### CSV Upload
- `POST /upload-csv` - Upload CSV file with employee events
- Accepts multipart/form-data with CSV file

### Scores
- `GET /scores?start=YYYY-MM-DD&end=YYYY-MM-DD` - Get employee scores for date range

## Sample CSV Format

```csv
date,employee_id,event_type,value,notes
2024-01-01,EMP001 - Paijo,delivery_success,10.0,Delivered on time
2024-01-02,EMP001 - Paijo,customer_rating,4.5,Good service
2024-01-03,EMP001 - Paijo,presence,1.0,Present
2024-01-04,EMP002 - Siti,complaint,1.0,Late delivery
```

## Scoring Metrics

- **Productivity** (40%): Total delivery_success values
- **Quality** (25%): Average customer_rating
- **Complaints Reduction** (20%): 100 - (complaints × 2)
- **Attendance** (15%): Percentage of presence events

Final score is weighted sum capped between 0-100.

## Running Tests

```bash
python -m pytest tests/
```