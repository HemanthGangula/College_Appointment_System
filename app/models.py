from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime
from typing import List

client = MongoClient('mongodb://localhost:27017/')
db = client.college_appointment_system

# Users Collection
def create_user(username: str, password: str, role: str, email: str) -> ObjectId:
    hashed_password = generate_password_hash(password)
    user = {
        "username": username,
        "password": hashed_password,
        "role": role,
        "email": email,
        "created_at": datetime.utcnow()
    }
    result = db.users.insert_one(user)
    return result.inserted_id

def authenticate_user(username: str, password: str = None):
    user = db.users.find_one({"username": username})
    if user and password:
        if check_password_hash(user['password'], password):
            return user
        return None
    return user

# Availability Collection
def add_availability(professor_id: str, date: str, time_slots: List[str]) -> ObjectId:
    availability_entry = {
        "professor_id": ObjectId(professor_id),
        "date": date,
        "time_slots": time_slots,
        "created_at": datetime.utcnow()
    }
    result = db.availability.insert_one(availability_entry)
    return result.inserted_id

def get_availability(date: str = None, professor_id: str = None):
    query = {}
    if date:
        query['date'] = date
    if professor_id:
        query['professor_id'] = ObjectId(professor_id)
    return list(db.availability.find(query))

# Appointments Collection
def book_appointment(student_id: str, professor_id: str, date: str, time_slot: str) -> ObjectId:
    appointment = {
        "student_id": ObjectId(student_id),
        "professor_id": ObjectId(professor_id),
        "date": date,
        "time_slot": time_slot,
        "created_at": datetime.utcnow()
    }
    result = db.appointments.insert_one(appointment)
    return result.inserted_id

def get_appointments(user_id: str, role: str):
    if role == 'student':
        query = {"student_id": ObjectId(user_id)}
    elif role == 'professor':
        query = {"professor_id": ObjectId(user_id)}
    else:
        query = {}
    return list(db.appointments.find(query))