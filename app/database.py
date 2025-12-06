from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class Employee:
    id: int
    name: str
    role: str
    branch: str = "Driver"

@dataclass
class Event:
    id: int
    employee_id: int
    date: str
    type: str
    value: float
    notes: str = ""

class InMemoryDB:
    def __init__(self):
        self.employees: Dict[int, Employee] = {}
        self.events: Dict[int, Event] = {}
        self.next_employee_id = 1
        self.next_event_id = 1
    
    def clear_data(self):
        self.employees.clear()
        self.events.clear()
        self.next_employee_id = 1
        self.next_event_id = 1
    
    def get_employee_by_role(self, role: str) -> Employee:
        for emp in self.employees.values():
            if emp.role == role:
                return emp
        return None
    
    def add_employee(self, name: str, role: str, branch: str = "Driver") -> int:
        emp_id = self.next_employee_id
        self.employees[emp_id] = Employee(emp_id, name, role, branch)
        self.next_employee_id += 1
        return emp_id
    
    def add_event(self, employee_id: int, date: str, event_type: str, value: float, notes: str = "") -> int:
        event_id = self.next_event_id
        self.events[event_id] = Event(event_id, employee_id, date, event_type, value, notes)
        self.next_event_id += 1
        return event_id
    
    def get_events_by_employee_and_date(self, employee_id: int, start_date: str, end_date: str) -> List[Event]:
        return [event for event in self.events.values() 
                if event.employee_id == employee_id and start_date <= event.date <= end_date]
    
    def get_all_employees(self) -> List[Employee]:
        return list(self.employees.values())

db = InMemoryDB()

def init_db():
    pass

def get_db():
    return db