# tests/test_appointments.py
import pytest
from flask import Flask
from app import create_app
from app.models import db, create_user, add_availability
from flask_jwt_extended import create_access_token
from bson import ObjectId

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
            db.drop_collection('appointments')
            # Create a test professor and student
            professor_id = create_user('professor', 'ProfPass123', 'professor', 'prof@example.com')
            student_id = create_user('student', 'StudentPass123', 'student', 'student@example.com')
            # Create access tokens
            client.professor_token = create_access_token(identity=str(professor_id))
            client.student_token = create_access_token(identity=str(student_id))
            # Add availability for professor
            add_availability(str(professor_id), '2023-10-15', ['10:00', '11:00'])
        yield client
        with app.app_context():
            # Teardown: Clear the test database
            db.drop_collection('users')
            db.drop_collection('availability')
            db.drop_collection('appointments')

def test_create_appointment_success(client):
    # Retrieve professor_id from the database
    professor = db.users.find_one({'username': 'professor'})
    student = db.users.find_one({'username': 'student'})
    
    response = client.post('/api/appointments', json={
        'professor_id': str(professor['_id']),
        'date': '2023-10-15',
        'time_slot': '10:00'
    }, headers={'Authorization': f'Bearer {client.student_token}'})
    
    assert response.status_code == 201
    assert 'appointment_id' in response.get_json()

def test_create_appointment_missing_fields(client):
    response = client.post('/api/appointments', json={
        'professor_id': '',
        'date': '2023-10-15'
        # Missing 'time_slot'
    }, headers={'Authorization': f'Bearer {client.student_token}'})
    
    assert response.status_code == 400
    assert response.get_json()['msg'] == 'Missing required fields'

def test_create_appointment_unavailable_slot(client):
    # First booking
    professor = db.users.find_one({'username': 'professor'})
    student = db.users.find_one({'username': 'student'})
    
    response1 = client.post('/api/appointments', json={
        'professor_id': str(professor['_id']),
        'date': '2023-10-15',
        'time_slot': '10:00'
    }, headers={'Authorization': f'Bearer {client.student_token}'})
    
    assert response1.status_code == 201
    
    # Second booking for the same slot
    response2 = client.post('/api/appointments', json={
        'professor_id': str(professor['_id']),
        'date': '2023-10-15',
        'time_slot': '10:00'
    }, headers={'Authorization': f'Bearer {client.student_token}'})
    
    assert response2.status_code == 400
    assert response2.get_json()['msg'] == 'Failed to create appointment'

def test_list_appointments_as_student(client):
    professor = db.users.find_one({'username': 'professor'})
    student = db.users.find_one({'username': 'student'})
    
    # Create an appointment
    appointment_id = db.appointments.insert_one({
        'student_id': ObjectId(student['_id']),
        'professor_id': ObjectId(professor['_id']),
        'date': '2023-10-15',
        'time_slot': '11:00',
        'created_at': '2023-10-01T10:00:00'
    }).inserted_id
    
    response = client.get('/api/appointments', query_string={
        'role': 'student'
    }, headers={'Authorization': f'Bearer {client.student_token}'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == str(appointment_id)
    assert data[0]['date'] == '2023-10-15'
    assert data[0]['time_slot'] == '11:00'

def test_list_appointments_as_professor(client):
    professor = db.users.find_one({'username': 'professor'})
    student = db.users.find_one({'username': 'student'})
    
    # Create an appointment
    appointment_id = db.appointments.insert_one({
        'student_id': ObjectId(student['_id']),
        'professor_id': ObjectId(professor['_id']),
        'date': '2023-10-15',
        'time_slot': '11:00',
        'created_at': '2023-10-01T10:00:00'
    }).inserted_id
    
    response = client.get('/api/appointments', query_string={
        'role': 'professor'
    }, headers={'Authorization': f'Bearer {client.professor_token}'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == str(appointment_id)
    assert data[0]['date'] == '2023-10-15'
    assert data[0]['time_slot'] == '11:00'

def test_list_appointments_pagination(client):
    professor = db.users.find_one({'username': 'professor'})
    student = db.users.find_one({'username': 'student'})
    
    # Create multiple appointments
    for i in range(15):
        db.appointments.insert_one({
            'student_id': ObjectId(student['_id']),
            'professor_id': ObjectId(professor['_id']),
            'date': f'2023-10-{10 + i}',
            'time_slot': f'{10 + i}:00',
            'created_at': '2023-10-01T10:00:00'
        })
    
    response = client.get('/api/appointments', query_string={
        'role': 'student',
        'page': 2,
        'limit': 10
    }, headers={'Authorization': f'Bearer {client.student_token}'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 5  # Total 15 appointments, page 2 should have 5