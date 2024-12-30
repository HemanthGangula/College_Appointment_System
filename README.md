# College Appointment System

## Problem Statement
Develop and deploy backend APIs for a college appointment system. The system allows:
- Professors to specify available time slots.
- Students to view available slots and book appointments.
- Authentication for both students and professors.
- Storage of user, availability, and appointment data.

## Technologies Used
- **Backend Framework**: Flask
- **Database**: MongoDB (local MongoDB container for development)
- **Authentication**: JWT
- **Deployment Targets**: AWS EC2 and AWS DocumentDB (final deployment)
- **Containerization**: Docker and Docker Compose
- **Testing**: Pytest

## Development Plan
1. **Local Database Setup**
   - Use Docker to create a MongoDB container for development.
   - Design a schema for users, availability, and appointments.

2. **Backend Development**
   - Develop RESTful APIs using Flask.
   - Implement the following APIs:
     - User authentication (login/signup).
     - Add/view availability (professors).
     - View/book appointments (students).
   - Use JWT for secure authentication.

3. **Containerization**
   - Create Dockerfiles for the backend service and MongoDB.
   - Use Docker Compose to manage multi-container setup locally.

4. **Testing**
   - Write test cases using Pytest for API endpoints.
   - Test the API flow manually using Postman or similar tools.

5. **Deployment**
   - Transition from MongoDB to AWS DocumentDB for production.
   - Deploy the backend API to AWS EC2.
   - Use environment variables for secrets and configuration.

## Local Development Steps
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd college-appointment-system
   ```

2. **Set Up MongoDB Container**
   - Ensure Docker is installed and running.
   - Start a MongoDB container:
     ```bash
     docker run -d --name mongodb -p 27017:27017 mongo
     ```

3. **Install Dependencies**
   - Create a Python virtual environment and install dependencies:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Run the Flask App**
   - Start the development server:
     ```bash
     flask run
     ```
   - Access the API at `http://127.0.0.1:5000`.

5. **Testing**
   - Run test cases:
     ```bash
     pytest
     ```

6. **Docker Compose Setup** (Optional for local testing)
   - Use Docker Compose to run both backend and database:
     ```bash
     docker-compose up
     
