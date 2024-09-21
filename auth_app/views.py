from django.shortcuts import render
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .arangodb_config import ArangoDBConfig
import logging


def home_view(request):
    return render(request, 'home.html')


def hello_view(request):
    # Fetch the username from the session
    username = request.session.get('username', 'Guest')
    return render(request, 'hello.html', {'username': username})



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        otp = random.randint(100000, 999999)  # OTP generation

        db = ArangoDBConfig()

        # Store user in ArangoDB with unverified status
        db.insert_user({
            'username': username,
            'email': email,
            'password': password,
            'otp': otp,
            'verified': False
        })

        # Send OTP via email
        send_mail(
            'Your OTP Code',
            f'Your OTP is {otp}',
            'from@example.com',
            [email]
        )

        # Log the email being stored in the session
        logging.debug(f"Storing email in session: {email}")

        # Store the email in the session for OTP verification
        request.session['email'] = email
        return redirect('otp')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user by checking ArangoDB
        db = ArangoDBConfig()
        user = db.get_user_by_username(username)

        if user and user['password'] == password and user['verified']:
            # Create a session
            request.session['username'] = username
            return redirect('hello')
        else:
            return render(request, 'login.html', {'error': 'Login failed. Please check your credentials or verify your account.'})

    return render(request, 'login.html')

def otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']  # The OTP entered by the user
        email = request.session.get('email')  # Get the email stored during registration

        logging.debug(f"Entered OTP: {entered_otp}, Email from session: {email}")

        db = ArangoDBConfig()
        user = db.get_user_by_email(email)

        if user:
            logging.debug(f"Stored OTP: {user['otp']}, Entered OTP: {entered_otp}")

            # Compare stored OTP with the entered OTP
            if str(user['otp']) == str(entered_otp):
                # OTP is correct, now verify the user
                if db.verify_user(email, entered_otp):
                    logging.debug(f"User {email} verified successfully.")
                    return redirect('login')  # Redirect to login page if verification succeeds
                else:
                    logging.debug(f"Failed to verify user {email}.")
                    return render(request, 'otp.html', {'error': 'Failed to verify the user. Try again.'})
            else:
                logging.debug(f"OTP mismatch: Entered OTP {entered_otp}, Stored OTP {user['otp']}")
                return render(request, 'otp.html', {'error': 'Incorrect OTP. Please try again.'})
        else:
            logging.debug(f"No user found with email: {email}")
            return render(request, 'otp.html', {'error': 'No user found with this email. Please register again.'})

    return render(request, 'otp.html')
