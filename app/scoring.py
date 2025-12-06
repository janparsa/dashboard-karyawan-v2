from app.database import get_db
from typing import Dict, Any

# Hardcoded scoring config
SCORING_CONFIG = {
    "productivity": 0.35,
    "quality": 0.25,
    "attendance": 0.25,
    "complaints_reduction": 0.15
}

def load_scoring_config() -> Dict[str, float]:
    return SCORING_CONFIG

def calculate_score(employee_id: int, start_date: str, end_date: str) -> Dict[str, Any]:
    config = load_scoring_config()
    
    db = get_db()
    events = db.get_events_by_employee_and_date(employee_id, start_date, end_date)
    
    # Calculate metrics based on new event types
    delivery_count = sum(event.value for event in events if event.type == 'Delivery_Count')
    
    on_time_events = [event.value for event in events if event.type == 'On_Time_Delivery_Rate']
    on_time_rate = sum(on_time_events) / len(on_time_events) if on_time_events else 0
    
    rating_events = [event.value for event in events if event.type == 'Customer_Rating_Avg']
    customer_rating = sum(rating_events) / len(rating_events) if rating_events else 0
    
    fuel_events = [event.value for event in events if event.type == 'Fuel_Efficiency_km_per_liter']
    fuel_efficiency = sum(fuel_events) / len(fuel_events) if fuel_events else 0
    
    # Normalize metrics to 0-100 scale based on actual data ranges
    # Delivery Count: 55-128 range, normalize to 0-100
    productivity = min(100, max(0, ((delivery_count - 50) / 80) * 100))  # 50-130 range
    
    # Customer Rating: 4.0-5.0 range, normalize to 0-100
    quality = max(0, ((customer_rating - 3.5) / 1.5) * 100)  # 3.5-5.0 to 0-100
    
    # On Time Rate: Already percentage 87-98%
    attendance = on_time_rate
    
    # Fuel Efficiency: 8-15 km/l range, normalize to 0-100
    complaints_reduction = min(100, max(0, ((fuel_efficiency - 7) / 8) * 100))  # 7-15 range
    
    # Calculate weighted score
    score_total = (
        productivity * config['productivity'] +
        quality * config['quality'] +
        complaints_reduction * config['complaints_reduction'] +
        attendance * config['attendance']
    )
    
    # Cap between 0-100
    score_total = max(0, min(100, score_total))
    
    details = {
        'productivity': round(productivity, 1),
        'quality': round(quality, 1),
        'complaints_reduction': round(complaints_reduction, 1),
        'attendance': round(attendance, 1),
        'delivery_count': delivery_count,
        'customer_rating': customer_rating,
        'on_time_rate': on_time_rate,
        'fuel_efficiency': fuel_efficiency
    }
    
    return {
        'score_total': round(score_total, 2),
        'details': details
    }