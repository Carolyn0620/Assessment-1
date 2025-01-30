from database import mycursor, mydb
import hashlib
from utils import get_valid_input, validate_current_username, validate_new_username, validate_password, validate_tel_no, validate_address, is_string

# Function to register a new user
def register_user(name, personal_id, tel_no, address, username, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "INSERT INTO users (name, personal_id, tel_no, address, username, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (name, personal_id, tel_no, address, username, hashed_password, role)
    mycursor.execute(sql, val)
    mydb.commit()
    print(f"{role.capitalize()} registered successfully.")

# Function to login a user
def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username, hashed_password)
    mycursor.execute(sql, val)
    return mycursor.fetchone()

# Function to log queries
def log_query(sql, val=None):
    log_sql = "INSERT INTO query_log (query, query_values) VALUES (%s, %s)"
    log_val = (sql, str(val) if val else 'NULL')
    mycursor.execute(log_sql, log_val)
    mydb.commit()

# Function to modify personal details
def modify_personal_details():
    while True:
        # Force a valid current username before proceeding
        current_username = validate_current_username()

        # Proceed only if the username exists
        new_name = get_valid_input("Enter your new name: ", is_string)
        new_username = get_valid_input("Enter new username: ", validate_new_username)
        new_password = get_valid_input("Enter new password (leave blank to keep current password): ", validate_password)
        new_personal_id = input("Enter Personal ID: ")
        new_tel_no = get_valid_input("Enter new telephone number: ", validate_tel_no)
        new_address = get_valid_input("Enter new address: ", validate_address)

        # Confirm data entry before saving changes
        print("\nPlease confirm your details:")
        print(f"New Name: {new_name}")
        print(f"New Username: {new_username}")
        print(f"New Personal ID: {new_personal_id}")
        print(f"New Telephone Number: {new_tel_no}")
        print(f"New Address: {new_address}")
        if new_password:
            print(f"New Password: {'*' * len(new_password)}")  # Display asterisks for password
        else:
            print("New Password: (Unchanged)")

        confirm = input("Are these details correct? (Y/N): ")
        if confirm.lower() == 'y':
            # Hash new password if provided
            if new_password:
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            else:
                # Retrieve the current hashed password
                sql_get_password = "SELECT password FROM users WHERE username = %s"
                mycursor.execute(sql_get_password, (current_username,))
                result = mycursor.fetchone()
                hashed_password = result[0] if result else None  # Avoid crashing

            # Update user details
            sql = """
            UPDATE users 
            SET name = %s, username = %s, password = %s, personal_id = %s, tel_no = %s, address = %s
            WHERE username = %s
            """
            val = (new_name, new_username, hashed_password, new_personal_id, new_tel_no, new_address, current_username)
            mycursor.execute(sql, val)
            mydb.commit()

            print("✅ Personal details updated successfully.")
            break
        else:
            reenter = input("Changes not saved. Re-enter the details? (Y/N): ")
            if reenter.lower() == 'y':
                continue  # This will loop back to re-enter personal details
            else:
                break