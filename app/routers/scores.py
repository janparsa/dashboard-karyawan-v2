from fastapi import APIRouter, Query
from app.database import get_db
from app.scoring import calculate_score
from app.schemas import ScoreResponse
from typing import List

router = APIRouter()

@router.get("/scores", response_model=List[ScoreResponse])
async def get_scores(
    start: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end: str = Query(..., description="End date (YYYY-MM-DD)")
):
    db = get_db()
    employees = db.get_all_employees()
    
    # If no employees exist, return empty list
    if not employees:
        return []
    
    scores = []
    for employee in employees:
        score_data = calculate_score(employee.id, start, end)
        scores.append(ScoreResponse(
            employee_id=employee.id,
            name=f"{employee.role} - {employee.name}",
            score_total=score_data['score_total'],
            details=score_data['details']
        ))
    
    # Sort by score descending
    scores.sort(key=lambda x: x.score_total, reverse=True)
    
    return scores