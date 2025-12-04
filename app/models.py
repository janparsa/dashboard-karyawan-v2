from pydantic import BaseModel
from typing import Optional, Dict, Any

class Employee(BaseModel):
    id: int
    name: str
    role: str
    branch: str

class Event(BaseModel):
    id: Optional[int] = None
    employee_id: int
    date: str
    type: str
    value: float
    notes: Optional[str] = None

class Score(BaseModel):
    employee_id: int
    name: str
    score_total: float
    details: Dict[str, Any]