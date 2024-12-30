from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.models import add_availability, get_availability

availability_bp = Blueprint('availability', __name__)

@availability_bp.route('/availability', methods=['POST'])
@jwt_required()
def create_availability():
    user_id = get_jwt_identity()
    data = request.get_json()
    date = data.get('date')
    time_slots = data.get('time_slots')
    
    if not date or not time_slots:
        return jsonify({"msg": "Missing required fields"}), 400
    
    # Additional role verification can be added here
    availability_id = add_availability(user_id, date, time_slots)
    return jsonify({"availability_id": str(availability_id)}), 201

@availability_bp.route('/availability', methods=['GET'])
@jwt_required()
def list_availability():
    date = request.args.get('date')
    professor_id = request.args.get('professor_id')
    
    availability = get_availability(date, professor_id)
    formatted_availability = []
    
    for entry in availability:
        entry['_id'] = str(entry['_id'])
        entry['professor_id'] = str(entry['professor_id'])
        formatted_availability.append(entry)
    
    return jsonify(formatted_availability), 200