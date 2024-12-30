# College Appointment System API Documentation

## Authentication Endpoints

### Signup
- **Endpoint:** `/api/signup`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
    ```json
    {
        "username": "string",
        "password": "string",
        "role": "string (student/professor)",
        "email": "string"
    }
    ```
- **Responses:**
    - `201`: Success
        ```json
        {
            "msg": "User created successfully",
            "user_id": "string"
        }
        ```
    - `400`: `{"msg": "Missing required fields"}`
    - `409`: `{"msg": "User already exists"}`

### Login
- **Endpoint:** `/api/login`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```
- **Responses:**
    - `200`: `{"access_token": "string"}`
    - `401`: `{"msg": "Invalid credentials"}`

## Availability Endpoints

### Create Availability
- **Endpoint:** `/api/availability`
- **Method:** `POST`
- **Headers:**
    - `Content-Type: application/json`
    - `Authorization: Bearer <access_token>`
- **Request Body:**
    ```json
    {
        "date": "YYYY-MM-DD",
        "time_slots": ["HH:MM"]
    }
    ```
- **Responses:**
    - `201`: `{"availability_id": "string"}`
    - `400`: `{"msg": "Missing required fields"}`
    - `401`: `{"msg": "Missing Authorization Header"}`

### List Availability
- **Endpoint:** `/api/availability`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Query Parameters:**
    - `date` (optional)
    - `professor_id` (optional)
- **Responses:**
    - `200`: List of availability objects
    - `401`: `{"msg": "Missing Authorization Header"}`

## Appointment Endpoints

### Create Appointment
- **Endpoint:** `/api/appointments`
- **Method:** `POST`
- **Headers:**
    - `Content-Type: application/json`
    - `Authorization: Bearer <access_token>`
- **Request Body:**
    ```json
    {
        "professor_id": "string",
        "date": "YYYY-MM-DD",
        "time_slot": "HH:MM"
    }
    ```
- **Responses:**
    - `201`: `{"appointment_id": "string"}`
    - `400`: `{"msg": "Missing required fields"}`
    - `401`: `{"msg": "Missing Authorization Header"}`

### List Appointments
- **Endpoint:** `/api/appointments`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Query Parameters:**
    - `role` (optional, student/professor)
- **Responses:**
    - `200`: List of appointment objects
    - `401`: `{"msg": "Missing Authorization Header"}`

## Root Endpoint
- **Endpoint:** `/`
- **Method:** `GET`
- **Response:** `200: "Welcome to the College Appointment System"`

## Authentication Flow
1. Signup using POST `/api/signup`
2. Login using POST `/api/login`
3. Use received access_token in Authorization header
4. Access protected endpoints with the token

## Environment Requirements
- `JWT_SECRET_KEY`: Required for JWT token generation
- `HTTPS`: Required in production

## Security Recommendations
- Use strong JWT_SECRET_KEY in production
- Enable HTTPS in production
- Implement role-based access control
- Add pagination for list endpoints
- Implement thorough input validation
