from fastapi import APIRouter, Query
from app.database import get_db
from typing import List, Dict, Any

router = APIRouter()

@router.get("/analytics/suggestions")
async def get_suggestions(
    start: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end: str = Query(..., description="End date (YYYY-MM-DD)")
):
    db = get_db()
    employees = db.get_all_employees()
    
    employees_data = []
    for emp in employees:
        events = db.get_events_by_employee_and_date(emp.id, start, end)
        
        delivery_events = [e.value for e in events if e.type == 'Delivery_Count']
        rating_events = [e.value for e in events if e.type == 'Customer_Rating_Avg']
        ontime_events = [e.value for e in events if e.type == 'On_Time_Delivery_Rate']
        fuel_events = [e.value for e in events if e.type == 'Fuel_Efficiency_km_per_liter']
        
        employees_data.append({
            'name': emp.name,
            'role': emp.role,
            'avg_deliveries': sum(delivery_events) / len(delivery_events) if delivery_events else None,
            'avg_rating': sum(rating_events) / len(rating_events) if rating_events else None,
            'avg_ontime': sum(ontime_events) / len(ontime_events) if ontime_events else None,
            'avg_fuel': sum(fuel_events) / len(fuel_events) if fuel_events else None
        })
    
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