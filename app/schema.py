# app/schema.py
from datetime import datetime
from bson import ObjectId
from typing import List
from werkzeug.security import generate_password_hash
from re import match

class BaseModel:
    def __init__(self):
        self._id = ObjectId()
        self.created_at = datetime.utcnow()

class User(BaseModel):
    def __init__(self, username: str, password: str, role: str, email: str):
        super().__init__()
        if role not in ['student', 'professor']:
            raise ValueError("Role must be 'student' or 'professor'")
        if not match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.email = email

    def __repr__(self):
        return f"User(username={self.username}, role={self.role}, email={self.email})"

class Availability(BaseModel):
    def __init__(self, professor_id: ObjectId, date: str, time_slots: List[str] = None):
        super().__init__()
        self.professor_id = professor_id
        self.date = date  # Format: YYYY-MM-DD
        self.time_slots = time_slots if time_slots else []

    def __repr__(self):
        return f"Availability(professor_id={self.professor_id}, date={self.date})"

class Appointment(BaseModel):
    def __init__(self, student_id: ObjectId, professor_id: ObjectId, date: str, time_slot: str):
        super().__init__()
        self.student_id = student_id
        self.professor_id = professor_id
        self.date = date  # Format: YYYY-MM-DD
        self.time_slot = time_slot

    def __repr__(self):
        return f"Appointment(student_id={self.student_id}, professor_id={self.professor_id}, date={self.date}, time_slot={self.time_slot})"