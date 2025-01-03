# app/routes/appointments.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import book_appointment, get_appointments, update_appointment_status_in_db

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    student_id = get_jwt_identity()
    professor_id = data.get('professor_id')
    date = data.get('date')
    time_slot = data.get('time_slot')
    
    if not all([professor_id, date, time_slot]):
        return jsonify({"msg": "Missing required fields"}), 400
    
    appointment_id = book_appointment(student_id, professor_id, date, time_slot)
    if appointment_id:
        return jsonify({"appointment_id": str(appointment_id)}), 201
    else:
        return jsonify({"msg": "Failed to create appointment"}), 400

@appointments_bp.route('/appointments', methods=['GET'])
@jwt_required()
def list_appointments():
    user_id = get_jwt_identity()
    role = request.args.get('role')

    appointments = get_appointments(user_id, role)
    if appointments is not None:
        return jsonify([
            {
                "id": str(appointment["_id"]),
                "student_id": str(appointment["student_id"]),
                "professor_id": str(appointment["professor_id"]),
                "date": appointment["date"],
                "time_slot": appointment["time_slot"],
                "status": appointment.get("status", "pending"),
                "created_at": appointment["created_at"].isoformat()
            }
            for appointment in appointments
        ]), 200
    else:
        return jsonify({"msg": "Failed to retrieve appointments"}), 400

@appointments_bp.route('/appointments/<appointment_id>/status', methods=['PUT'])
@jwt_required()
def update_appointment_status(appointment_id):
    data = request.get_json()
    status = data.get('status')  # 'accepted' or 'canceled'

    # Logic to update appointment status
    updated = update_appointment_status_in_db(appointment_id, status)
    if updated:
        return jsonify({"msg": "Appointment status updated."}), 200
    else:
        return jsonify({"msg": "Failed to update appointment."}), 400

def format_appointment(appointment):
    return {
        "id": appointment.id,
        "student_id": appointment.student_id,
        "professor_id": appointment.professor_id,
        "date": appointment.date,
        "time_slot": appointment.time_slot,
        "status": appointment.status if appointment.status else "pending"
    }