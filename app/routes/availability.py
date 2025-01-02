# app/routes/availability.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import add_availability, get_availability
from datetime import datetime

availability_bp = Blueprint('availability', __name__)

@availability_bp.route('/availability', methods=['POST'])
@jwt_required()
def create_availability():
    data = request.get_json()
    professor_id = get_jwt_identity()
    date = data.get('date')
    time_slots = data.get('time_slots', [])

    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD."}), 400

    availability_id = add_availability(professor_id, date, time_slots)
    if availability_id:
        return jsonify({"availability_id": str(availability_id)}), 201
    else:
        return jsonify({"msg": "Failed to create availability"}), 400

@availability_bp.route('/availability', methods=['GET'])
@jwt_required()
def list_availability():
    date = request.args.get('date')
    professor_id = request.args.get('professor_id')

    availability = get_availability(date, professor_id)
    return jsonify(availability), 200