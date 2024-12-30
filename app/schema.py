from datetime import datetime
from bson import ObjectId
from typing import List

class User:
    def __init__(self, username: str, password: str, role: str, email: str):
        self._id = ObjectId()
        self.username = username
        self.password = password  # Ensure to hash the password
        self.role = role  # 'student' or 'professor'
        self.email = email
        self.created_at = datetime.utcnow()

class Availability:
    def __init__(self, professor_id: ObjectId, date: str, time_slots: List[str]):
        self._id = ObjectId()
        self.professor_id = professor_id
        self.date = date  # Format: YYYY-MM-DD
        self.time_slots = time_slots  # Example: ["09:00", "10:00", "11:00"]
        self.created_at = datetime.utcnow()

class Appointment:
    def __init__(self, student_id: ObjectId, professor_id: ObjectId, date: str, time_slot: str):
        self._id = ObjectId()
        self.student_id = student_id
        self.professor_id = professor_id
        self.date = date  # Format: YYYY-MM-DD
        self.time_slot = time_slot  # Example: "09:00"
        self.created_at = datetime.utcnow()