# tests/test_availability.py
import pytest
from flask import Flask
from app import create_app
from app.models import db, create_user, add_availability
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_college_appointment_system'
    with app.test_client() as client:
        with app.app_context():
            # Setup: Clear the test database
            db.drop_collection('users')
            db.drop_collection('availability')
            # Create a test user and generate token
            user_id = create_user('professor', 'ProfPass123', 'professor', 'prof@example.com')
            token = create_access_token(identity=str(user_id))
            client.token = token
        yield client
        with app.app_context():
            # Teardown: Clear the test database
            db.drop_collection('users')
            db.drop_collection('availability')

def test_create_availability_success(client):
    response = client.post('/api/availability', json={
        'date': '2023-10-15',
        'time_slots': ['10:00', '11:00']
    }, headers={'Authorization': f'Bearer {client.token}'})
    assert response.status_code == 201
    assert 'availability_id' in response.get_json()

def test_create_availability_missing_fields(client):
    response = client.post('/api/availability', json={
        # Missing 'date'
        'time_slots': ['10:00', '11:00']
    }, headers={'Authorization': f'Bearer {client.token}'})
    assert response.status_code == 400
    assert response.get_json()['msg'] == 'Failed to create availability'

def test_create_availability_unauthorized(client):
    response = client.post('/api/availability', json={
        'date': '2023-10-15',
        'time_slots': ['10:00', '11:00']
    })
    assert response.status_code == 401

def test_list_availability_success(client):
    # Add availability first
    add_availability('professor_id', '2023-10-15', ['10:00', '11:00'])
    
    response = client.get('/api/availability', query_string={
        'date': '2023-10-15',
        'professor_id': 'professor_id'
    }, headers={'Authorization': f'Bearer {client.token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['date'] == '2023-10-15'
    assert data[0]['time_slots'] == ['10:00', '11:00']

def test_list_availability_no_results(client):
    response = client.get('/api/availability', query_string={
        'date': '2023-12-01',
        'professor_id': 'professor_id'
    }, headers={'Authorization': f'Bearer {client.token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_list_availability_unauthorized(client):
    response = client.get('/api/availability', query_string={
        'date': '2023-10-15',
        'professor_id': 'professor_id'
    })
    assert response.status_code == 401