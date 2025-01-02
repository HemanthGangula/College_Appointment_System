# app/models.py
import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime
from typing import List
# from flask_cors import CORS  # Remove this import

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/college_appointment_system')
client = MongoClient(MONGO_URI)
db = client.college_appointment_system

# Remove the incorrect CORS initialization
# CORS(db)

# User Functions
def create_user(username: str, password: str, role: str, email: str) -> ObjectId:
    hashed_password = generate_password_hash(password)
    user = {
        "username": username,
        "password": hashed_password,
        "role": role,
        "email": email,
        "created_at": datetime.utcnow()
    }
    try:
        result = db.users.insert_one(user)
        return result.inserted_id
    except PyMongoError as e:
        print(f"Error creating user: {e}")
        return None

def authenticate_user(username: str, password: str = None):
    user = db.users.find_one({"username": username})
    if user and password and check_password_hash(user['password'], password):
        return user
    return None

# Availability Functions
def add_availability(professor_id: str, date: str, time_slots: List[str]) -> ObjectId:
    availability_entry = {
        "professor_id": ObjectId(professor_id),
        "date": date,
        "time_slots": time_slots,
        "created_at": datetime.utcnow()
    }
    try:
        result = db.availability.insert_one(availability_entry)
        return result.inserted_id
    except PyMongoError as e:
        print(f"Error adding availability: {e}")
        return None

def get_availability(date: str = None, professor_id: str = None):
    query = {}
    if date:
        query['date'] = date
    if professor_id:
        query['professor_id'] = ObjectId(professor_id)
    return list(db.availability.find(query))

# Appointment Functions
def book_appointment(student_id: str, professor_id: str, date: str, time_slot: str) -> ObjectId:
    try:
        # Ensure the slot is available
        availability = db.availability.find_one_and_update(
            {"professor_id": ObjectId(professor_id), "date": date, "time_slots": time_slot},
            {"$pull": {"time_slots": time_slot}}
        )

        if not availability:
            raise ValueError("The selected time slot is not available.")

        # Create the appointment
        appointment = {
            "student_id": ObjectId(student_id),
            "professor_id": ObjectId(professor_id),
            "date": date,
            "time_slot": time_slot,
            "created_at": datetime.utcnow()
        }

        result = db.appointments.insert_one(appointment)
        return result.inserted_id
    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    except PyMongoError as e:
        print(f"Error booking appointment: {e}")
        return None

def get_appointments(user_id: str, role: str, page: int = 1, limit: int = 10):
    try:
        query = {}
        if role == "student":
            query["student_id"] = ObjectId(user_id)
        elif role == "professor":
            query["professor_id"] = ObjectId(user_id)

        # Pagination logic
        skip = (page - 1) * limit
        appointments = db.appointments.find(query).skip(skip).limit(limit)

        # Format the appointments
        return [
            {
                "id": str(appointment["_id"]),
                "student_id": str(appointment["student_id"]),
                "professor_id": str(appointment["professor_id"]),
                "date": appointment["date"],
                "time_slot": appointment["time_slot"],
                "created_at": appointment["created_at"]
            }
            for appointment in appointments
        ]
    except PyMongoError as e:
        print(f"Error fetching appointments: {e}")
        return []

def update_appointment_status_in_db(appointment_id: str, status: str) -> bool:
    if status not in ['accepted', 'canceled']:
        return False
    try:
        result = db.appointments.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"status": status}}
        )
        return result.modified_count > 0
    except PyMongoError as e:
        print(f"Error updating appointment status: {e}")
        return False

# Utility Functions
def format_appointment(appointment):
    """Format a single appointment document."""
    return {
        "id": str(appointment["_id"]),
        "student_id": str(appointment["student_id"]),
        "professor_id": str(appointment["professor_id"]),
        "date": appointment["date"],
        "time_slot": appointment["time_slot"],
        "created_at": appointment["created_at"]
    }