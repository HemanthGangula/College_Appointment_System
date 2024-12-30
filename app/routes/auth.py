from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import create_user, authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    email = data.get('email')
    
    if not all([username, password, role, email]):
        return jsonify({"msg": "Missing required fields"}), 400
    
    if role not in ['student', 'professor']:
        return jsonify({"msg": "Invalid role"}), 400
    
    existing_user = authenticate_user(username)
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409
    
    user_id = create_user(username, password, role, email)
    return jsonify({"msg": "User created successfully", "user_id": str(user_id)}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({"msg": "Missing username or password"}), 400
    
    user = authenticate_user(username, password)
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({"access_token": access_token}), 200