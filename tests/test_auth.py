# tests/test_auth.py
import pytest
from flask import Flask
from app import create_app
from app.models import db, create_user
from flask_jwt_extended import decode_token

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_college_appointment_system'
    with app.test_client() as client:
        with app.app_context():
            # Setup: Clear the test database
            db.drop_collection('users')
        yield client
        with app.app_context():
            # Teardown: Clear the test database
            db.drop_collection('users')

def test_signup_success(client):
    response = client.post('/api/signup', json={
        'username': 'testuser',
        'password': 'TestPass123',
        'role': 'student',
        'email': 'testuser@example.com'
    })
    assert response.status_code == 201
    assert response.get_json()['msg'] == 'User created successfully'

def test_signup_missing_fields(client):
    response = client.post('/api/signup', json={
        'username': 'testuser',
        'password': 'TestPass123',
        # Missing 'role' and 'email'
    })
    assert response.status_code == 400
    assert response.get_json()['msg'] == 'User creation failed'

def test_login_success(client):
    # First, create a user
    create_user('testuser', 'TestPass123', 'student', 'testuser@example.com')
    
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'TestPass123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    # Verify the token
    token_data = decode_token(data['access_token'])
    assert 'identity' in token_data

def test_login_invalid_credentials(client):
    response = client.post('/api/login', json={
        'username': 'nonexistent',
        'password': 'WrongPass'
    })
    assert response.status_code == 401
    assert response.get_json()['msg'] == 'Invalid credentials'