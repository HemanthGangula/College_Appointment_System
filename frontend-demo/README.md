# Frontend Demo

This folder contains a minimal frontend to demonstrate the functionality of the College Appointment System backend.

## Files

- `index.html`: Welcome page with navigation links to Sign Up and Login.
- `signup.html`: Sign Up form to create a new user.
- `login.html`: Login form to authenticate a user.
- `styles.css`: Basic styling for the frontend pages.

## Usage

1. **Start the Backend Server**
   
   Ensure that your Flask backend server is running on `http://localhost:5000`.

2. **Open the Frontend Pages**
   
   - Open `index.html` in your web browser to access the welcome page.
   - Navigate to `signup.html` to create a new user.
   - Navigate to `login.html` to authenticate.

## Notes

- This frontend is for prototype and testing purposes only.
- The access token received upon successful login is stored in the browser's `localStorage` and can be used for authenticated requests to other endpoints.
- Ensure that CORS is properly configured on the backend to allow requests from the frontend.
