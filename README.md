# token_qms
QMS in python

### Hospital OPD Scheduler with Token Management System

This project is a Flask-based web application designed to streamline the appointment booking process in a hospital's Outpatient Department (OPD). The system allows patients to schedule appointments with various departments, while providing a token-based queuing system. The application also includes administrative functionality for managing departments and tokens, and a doctor's terminal for handling patient flow.

#### Key Features:

1. **Homepage (Token Generation)**
   - **Department Selection:** Patients can select the desired department for their appointment from a list of available departments.
   - **Patient Name and Date Selection:** Patients enter their name and select an appointment date.
   - **Token Generation:** After submitting the form, the system generates a token, displaying the token number, department, patient name, and appointment date.

2. **Admin Page**
   - **Manage Departments:** Admins can add new departments (e.g., Orthopedic Surgery, Rheumatology, etc.) to the system.
   - **Manage Tokens:** Admins can view, delete, and monitor all tokens across various departments. The admin interface displays detailed information about each token, including patient name, department, and status.

3. **Current Token Progress**
   - A dedicated page that shows the current token in progress for each department. This helps in monitoring the ongoing appointments department-wise.

4. **Doctor's Terminal**
   - **Current Token Management:** Doctors can view the current token number in progress and move to the next token.
   - **Time Tracking:** The system tracks the time spent on each token, providing insights into patient handling efficiency.
   - **Control Buttons:** Doctors have buttons to close the current token and move on to the next one.

5. **Database Management**
   - The application uses SQLite as the backend database. The schema includes tables for managing departments and tokens, with relationships defined between them.
   - A migration script is provided to update the database schema, adding new columns (e.g., `appointment_date`) as needed.

6. **Error Handling and Notifications**
   - The application includes basic error handling (e.g., missing fields in forms) and user-friendly notifications through Flask’s flash messaging system.
   - Ensures that patients can only book appointments with available departments and on valid dates.

7. **User Interface**
   - Simple and intuitive HTML templates are used for different parts of the application, including the homepage, admin page, token display page, and doctor's terminal.
   - Links between different parts of the system allow seamless navigation, such as returning to the homepage from the admin or doctor's terminal.

8. **Security and Deployment**
   - The application uses Flask’s built-in session management for basic security.
   - Flask’s debug mode can be used for local development, and the app can be deployed to production environments with additional configurations.

This project offers a functional, easy-to-use system for hospital staff and patients to manage OPD appointments effectively, while keeping track of token queues and departmental appointments.
