import hashlib
from utils import Validator
from user import User
import sqlite3
from database import Database

def add_user_to_db(name, personal_id, tel_no, address, username, password, role):
    # Add a new user to the database securely.
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()

    # Create an instance of the User class to use its method
    user = User(name, personal_id, tel_no, address, username, password, role)
    # Hash the password before saving
    hashed_password = user.hash_password(password)  # Correctly calling the instance method

    try:
        sql = "INSERT INTO users (name, personal_id, tel_no, address, username, password, role) VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (name, personal_id, tel_no, address, username, hashed_password, role)
        cursor.execute(sql, values)
        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return "Username already exists. Please try a different username."
    finally:
        connection.close()



def get_user_from_db(username, password):

    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()

    sql = "SELECT id, name, personal_id, tel_no, address, username, password, role FROM users WHERE username = ?"
    cursor.execute(sql, (username,))
    user_data = cursor.fetchone()
          
    connection.close()

    if user_data:
        # Destructure the data and pass the hashed password
        user_id, name, personal_id, tel_no, address, username, hashed_password, role = user_data
        user = User(name, personal_id, tel_no, address, username, hashed_password, role, user_id)

        if user.verify_password(password):
            return user  # Return a User object instead of a tuple
        else:
            return None  # Invalid password
    return None  # User not found

def validate_username(name):
    if not name.isalnum():
        print("Error: Username must be alphanumeric.")
        return False
    return True



