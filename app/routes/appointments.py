from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.models import book_appointment, get_appointments

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
    return jsonify({"appointment_id": str(appointment_id)}), 201

@appointments_bp.route('/appointments', methods=['GET'])
@jwt_required()
def list_appointments():
    user_id = get_jwt_identity()
    role = request.args.get('role')
    
    appointments = get_appointments(user_id, role)
    formatted_appointments = []
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])
        appointment['student_id'] = str(appointment['student_id'])
        appointment['professor_id'] = str(appointment['professor_id'])
        formatted_appointments.append(appointment)
    
    return jsonify(formatted_appointments), 200