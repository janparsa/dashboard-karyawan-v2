import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.database import init_db
from app.routers import upload_csv, scores, analytics, blob_upload

app = FastAPI(title="Scoreboard Produktivitas SDM")

# Initialize in-memory database
init_db()

# Include routers
app.include_router(upload_csv.router)
app.include_router(scores.router)
app.include_router(analytics.router)
app.include_router(blob_upload.router)

@app.get("/")
async def root():
    return {"message": "Dashboard Karyawan API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# For Vercel
handler = app