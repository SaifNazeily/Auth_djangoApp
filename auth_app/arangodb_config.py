from arango import ArangoClient
import logging

class ArangoDBConfig:
    def __init__(self):
        # Initialize the ArangoDB client and connect to the database
        client = ArangoClient(hosts='http://localhost:8529')  # Adjust if needed
        self.db = client.db('user_info', username='root', password='yourpassword')

    # Insert user into ArangoDB with email, username, password, and OTP
    def insert_user(self, user_data):
        users_collection = self.db.collection('users')
        users_collection.insert(user_data)

    # Retrieve user by email for OTP verification
    def get_user_by_email(self, email):
        users_collection = self.db.collection('users')
        cursor = users_collection.find({'email': email})
    
        # Return the first result, or None if no result is found
        return next(cursor, None)

    # Retrieve user by username for login
    def get_user_by_username(self, username):
        users_collection = self.db.collection('users')
        cursor = users_collection.find({'username': username})
        
        # Return the first result, or None if no result is found
        return next(cursor, None)

    # Verify user by matching the OTP and setting the verified flag to True
    def verify_user(self, email, otp):
        users_collection = self.db.collection('users')

        # Convert the entered OTP to an integer (since the OTP is stored as a number in the database)
        try:
            otp = int(otp)
        except ValueError:
            logging.debug(f"Failed to convert entered OTP {otp} to integer.")
            return False

        # Log the email and OTP being searched for
        logging.debug(f"Searching for user with email: {email} and otp: {otp}")

        # Find the user by email and OTP
        cursor = users_collection.find({'email': email, 'otp': otp})
        user = next(cursor, None)

        if user:
            logging.debug(f"Found user with key: {user['_key']}, updating verified status.")

            # Update the user's verified status to True using _key
            try:
                # Use the correct structure for the update operation
                users_collection.update({'_key': user['_key'], 'verified': True})
                logging.debug(f"User with key {user['_key']} has been successfully verified.")
                return True
            except Exception as e:
                logging.debug(f"Error during update: {e}")
                return False

        logging.debug(f"Failed to find user with email: {email} and otp: {otp}")
        return False



    # Check if a user with the given email already exists
    def user_exists_by_email(self, email):
        users_collection = self.db.collection('users')
        cursor = users_collection.find({'email': email})
        user = next(cursor, None)
        return user is not None

    # Check if a user with the given username already exists
    def user_exists_by_username(self, username):
        users_collection = self.db.collection('users')
        cursor = users_collection.find({'username': username})
        user = next(cursor, None)
        return user is not None
