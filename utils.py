from database import Database

class Validator:

    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def get_valid_input(prompt, validation_func):
        while True:
            value = input(prompt).strip()
            if validation_func(value):
                return value
            else:
                print("Invalid input, please try again.")

    def is_positive_int(value):
        return value.isdigit() and int(value) > 0

    def is_string(value):
        return isinstance(value, str) and value.strip() != ""

    def validate_new_username(username, cursor):

        # Check if the new username is at least 3 characters long
        if len(username) < 3:
            print("Username must be at least 3 characters long. Please try again.")
            return False
        
        # Check if the new username is alphanumeric
        if not username.isalnum():
            print("Error: Username must be alphanumeric.")
            return False
        
        # Check if the new username already exists in the database
        try:
            sql_check_username = "SELECT username FROM users WHERE username = ?"
            cursor.execute(sql_check_username, (username,))
            existing_username = cursor.fetchone()

            if existing_username is not None:
                print("Username already taken. Please try again.")
                return False

            # If username is valid and not taken, return True
            return True

        except Exception as e:
            print(f"Error while checking username: {e}")
            return False
        
    def validate_password(password):
        # Password minimum length 6 characters
        if len(password) >= 6:
            return True
        return False

    def validate_tel_no(tel_no):
        # telephone number is at least 7 digits and consists entirely of digits
        if len(tel_no) >= 7 and tel_no.isdigit():
            return True
        return False

    def validate_address(address):
        # Check if the address is non-empty and has a reasonable length
        if len(address.strip()) > 0 and len(address) <= 200:
            return True
        return False