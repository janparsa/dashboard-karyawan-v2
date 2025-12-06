from fastapi import APIRouter, Query
from app.database import get_db
from typing import List, Dict, Any

router = APIRouter()

@router.get("/analytics/suggestions")
async def get_suggestions(
    start: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end: str = Query(..., description="End date (YYYY-MM-DD)")
):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get performance data
        cursor.execute("""
            SELECT e.name, e.role, 
                   AVG(CASE WHEN ev.type = 'Delivery_Count' THEN ev.value END) as avg_deliveries,
                   AVG(CASE WHEN ev.type = 'Customer_Rating_Avg' THEN ev.value END) as avg_rating,
                   AVG(CASE WHEN ev.type = 'On_Time_Delivery_Rate' THEN ev.value END) as avg_ontime,
                   AVG(CASE WHEN ev.type = 'Fuel_Efficiency_km_per_liter' THEN ev.value END) as avg_fuel
            FROM employees e
            JOIN events ev ON e.id = ev.employee_id
            WHERE ev.date BETWEEN %s AND %s
            GROUP BY e.id, e.name, e.role
        """, (start, end))
        
        employees_data = cursor.fetchall()
    
    suggestions = []
    
    for emp in employees_data:
        emp_suggestions = []
        
        # Delivery performance
        if emp['avg_deliveries'] and emp['avg_deliveries'] < 80:
            emp_suggestions.append({
                "type": "productivity",
                "message": f"Increase delivery count (current: {emp['avg_deliveries']:.0f}/day, target: 100+)",
                "priority": "high" if emp['avg_deliveries'] < 60 else "medium"
            })
        
        # Customer rating
        if emp['avg_rating'] and emp['avg_rating'] < 4.3:
            emp_suggestions.append({
                "type": "quality",
                "message": f"Improve customer service (current: {emp['avg_rating']:.2f}/5, target: 4.5+)",
                "priority": "high" if emp['avg_rating'] < 4.0 else "medium"
            })
        
        # On-time delivery
        if emp['avg_ontime'] and emp['avg_ontime'] < 92:
            emp_suggestions.append({
                "type": "attendance",
                "message": f"Improve on-time delivery (current: {emp['avg_ontime']:.1f}%, target: 95%+)",
                "priority": "high" if emp['avg_ontime'] < 88 else "medium"
            })
        
        # Fuel efficiency
        if emp['avg_fuel'] and emp['avg_fuel'] < 10:
            emp_suggestions.append({
                "type": "fuel_efficiency",
                "message": f"Improve fuel efficiency (current: {emp['avg_fuel']:.1f} km/l, target: 12+ km/l)",
                "priority": "medium"
            })
        
        if emp_suggestions:
            suggestions.append({
                "employee": emp['name'],
                "employee_code": emp['role'],
                "suggestions": emp_suggestions
            })
    
    return {
        "total_employees_analyzed": len(employees_data),
        "employees_needing_improvement": len(suggestions),
        "suggestions": suggestions
    }