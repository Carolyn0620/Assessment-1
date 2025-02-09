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

    # Hash the password before saving
    hashed_password = User.hash_password(password)

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
        user = User(*user_data)
        hashed_input_password = User.hash_password(password)
        print(f"Input password (hashed): {hashed_input_password}")
        print(f"Stored password (hashed): {user.password}")
        if user.verify_password(password):  # Verify password
            return user  # Return the User object if the password matches
        else:
            return None  # Invalid password
    return None  # User not found



def validate_username(name):
    if not name.isalnum():
        print("Error: Username must be alphanumeric.")
        return False
    return True

db = Database()
connection = db.connect_to_db()
cursor = connection.cursor()

# class User:
#     def __init__(self, name, personal_id, tel_no, address, username, password, role):
#         self.name = name
#         self.personal_id = personal_id
#         self.tel_no = tel_no
#         self.address = address
#         self.username = username
#         self.password = self.hash_password(password)
#         self.role = role

#     @staticmethod
#     def hash_password(password):
#         return hashlib.sha256(password.encode()).hexdigest()


#     @classmethod
#     def login(cls, username, password):
#         hashed_password = cls.hash_password(password)
#         sql = "SELECT * FROM users WHERE username = %s AND password = %s"
#         val = (username, hashed_password)
#         cursor.execute(sql, val)
#         user_data = cursor.fetchone()
#         if user_data:
#             return cls(*user_data[:7])
#         return None

#     @staticmethod
#     def modify_personal_details():
#         while True:
#             current_username = Validator.validate_current_username(cursor)

#             new_name = Validator.get_valid_input("Enter your new name: ", Validator.is_string)
#             new_username = Validator.get_valid_input("Enter new username: ", Validator.validate_new_username)
#             new_password = Validator.get_valid_input("Enter new password: ", Validator.validate_password)
#             new_personal_id = input("Enter Personal ID: ")
#             new_tel_no = Validator.get_valid_input("Enter new telephone number: ", Validator.validate_tel_no)
#             new_address = Validator.get_valid_input("Enter new address: ", Validator.validate_address)

#             print("\nPlease confirm your details:")
#             print(f"New Name: {new_name}")
#             print(f"New Username: {new_username}")
#             print(f"New Personal ID: {new_personal_id}")
#             print(f"New Telephone Number: {new_tel_no}")
#             print(f"New Address: {new_address}")
#             if new_password:
#                 print(f"New Password: {'*' * len(new_password)}")
#             else:
#                 print("New Password: (Unchanged)")

#             confirm = input("Are these details correct? (Y/N): ")
#             if confirm.lower() == 'y':
#                 if new_password:
#                     hashed_password = User.hash_password(new_password)
#                 else:
#                     sql_get_password = "SELECT password FROM users WHERE username = %s"
#                     cursor.execute(sql_get_password, (current_username,))
#                     result = cursor.fetchall()
#                     hashed_password = result[0][0] if result else None

#                 sql = """
#                 UPDATE users 
#                 SET name = %s, username = %s, password = %s, personal_id = %s, tel_no = %s, address = %s
#                 WHERE username = %s
#                 """
#                 val = (new_name, new_username, hashed_password, new_personal_id, new_tel_no, new_address, current_username)
#                 cursor.execute(sql, val)
#                 connection.commit()

#                 print("Personal details updated successfully.")
#                 break