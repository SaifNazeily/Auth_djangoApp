from django.db import models
from django.core.exceptions import ValidationError

# Optional: Function to validate email format
def validate_email(email):
    if '@' not in email:
        raise ValidationError("Invalid email address")

# This is just a placeholder for the structure you might want to use for a User
class User:
    def __init__(self, email, password, otp, verified=False):
        self.email = email
        self.password = password  # You should hash this in real projects
        self.otp = otp
        self.verified = verified

