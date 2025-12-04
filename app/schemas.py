from pydantic import BaseModel
from typing import List

class CSVUploadResponse(BaseModel):
    rows_inserted: int
    message: str

class ScoreResponse(BaseModel):
    employee_id: int
    name: str
    score_total: float
    details: dict