from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import init_db
from app.routers import upload_csv, scores, analytics

app = FastAPI(title="Scoreboard Produktivitas SDM")

# Initialize database
init_db()

# Include routers
app.include_router(upload_csv.router)
app.include_router(scores.router)
app.include_router(analytics.router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

@app.get("/health")
async def health():
    return {"status": "ok"}