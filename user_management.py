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

def update_personal_details():
        
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()
  
    while True:
        current_username = Validator.validate_current_username(cursor)

        new_name = Validator.get_valid_input("Enter your new name: ", Validator.is_string)
        new_username = Validator.get_valid_input("Enter new username: ", lambda value: Validator.validate_new_username(value, cursor))
        new_password = Validator.get_valid_input("Enter new password: ", Validator.validate_password)
        new_personal_id = input("Enter Personal ID: ")
        new_tel_no = Validator.get_valid_input("Enter new telephone number: ", Validator.validate_tel_no)
        new_address = Validator.get_valid_input("Enter new address: ", Validator.validate_address)
        new_role = Validator.get_valid_input("Enter new role: ", Validator.is_string)

        confirm = input("Are you sure these details correct? (Y/N): ")
        if confirm.lower() == 'y':
            user = User(new_name, new_personal_id, new_tel_no, new_address, new_username, new_password, new_role)
            hashed_password = user.hash_password(new_password)

            sql = """
            UPDATE users 
            SET name = ?, username = ?, password = ?, personal_id = ?, tel_no = ?, address = ?
            WHERE username = ?
            """
            val = (new_name, new_username, hashed_password, new_personal_id, new_tel_no, new_address, current_username)
            cursor.execute(sql, val)
            connection.commit()

            print("Personal details updated successfully.")
            break
        else:
            break