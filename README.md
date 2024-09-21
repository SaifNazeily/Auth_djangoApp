# Auth_Django Project

**Auth_Django** is a Django-based authentication system featuring email OTP verification and integration with ArangoDB for efficient user data management. It's designed to provide a customizable foundation for authentication workflows.

## Features
- **User Registration with OTP Verification**: Verifies users' email addresses via OTP during registration.
- **Login with Username & Password**: Secure login system once the user account is verified.
- **Session Management**: Supports session-based authentication.
- **ArangoDB Integration**: Uses ArangoDB for storing user data.
- **Logout Functionality**: Allows users to safely log out.

## Tech Stack
- **Backend**: Django 5.1.1
- **Database**: ArangoDB
- **Frontend**: HTML, Bootstrap
- **Email Service**: Uses SMTP for OTP email verification.

## Setup Instructions
To run this project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SaifNazeily/Auth_DjangoProject.git
   cd Auth_DjangoProject

2. **Create a virtual environment and activate it**
    python -m venv env
    source env/bin/activate  # On Linux/Mac
    env\Scripts\activate     # On Windows

3. **Install the dependencies:**
    pip install -r requirements.txt

4. **Apply specific Django migrations**
    python manage.py migrate auth
    python manage.py migrate sessions
    
5. **Run the development server**
    python manage.py runserver

