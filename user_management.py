import hashlib
from utils import Validator
from database import Database

# Get database instance
db_instance = Database()
mydb = db_instance.get_connection()
mycursor = db_instance.get_cursor()

class User:
    def __init__(self, name, personal_id, tel_no, address, username, password, role):
        self.name = name
        self.personal_id = personal_id
        self.tel_no = tel_no
        self.address = address
        self.username = username
        self.password = self.hash_password(password)
        self.role = role

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save_to_db(self):
        sql = "INSERT INTO users (name, personal_id, tel_no, address, username, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (self.name, self.personal_id, self.tel_no, self.address, self.username, self.password, self.role)
        mycursor.execute(sql, val)
        mydb.commit()
        print(f"{self.role.capitalize()} registered successfully.")

    @classmethod
    def login(cls, username, password):
        hashed_password = cls.hash_password(password)
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        val = (username, hashed_password)
        mycursor.execute(sql, val)
        user_data = mycursor.fetchone()
        if user_data:
            return cls(*user_data[:7])
        return None

    @staticmethod
    def modify_personal_details():
        while True:
            current_username = Validator.validate_current_username(mycursor)

            new_name = Validator.get_valid_input("Enter your new name: ", Validator.is_string)
            new_username = Validator.get_valid_input("Enter new username: ", Validator.validate_new_username)
            new_password = Validator.get_valid_input("Enter new password: ", Validator.validate_password)
            new_personal_id = input("Enter Personal ID: ")
            new_tel_no = Validator.get_valid_input("Enter new telephone number: ", Validator.validate_tel_no)
            new_address = Validator.get_valid_input("Enter new address: ", Validator.validate_address)

            print("\nPlease confirm your details:")
            print(f"New Name: {new_name}")
            print(f"New Username: {new_username}")
            print(f"New Personal ID: {new_personal_id}")
            print(f"New Telephone Number: {new_tel_no}")
            print(f"New Address: {new_address}")
            if new_password:
                print(f"New Password: {'*' * len(new_password)}")
            else:
                print("New Password: (Unchanged)")

            confirm = input("Are these details correct? (Y/N): ")
            if confirm.lower() == 'y':
                if new_password:
                    hashed_password = User.hash_password(new_password)
                else:
                    sql_get_password = "SELECT password FROM users WHERE username = %s"
                    mycursor.execute(sql_get_password, (current_username,))
                    result = mycursor.fetchall()
                    hashed_password = result[0][0] if result else None

                sql = """
                UPDATE users 
                SET name = %s, username = %s, password = %s, personal_id = %s, tel_no = %s, address = %s
                WHERE username = %s
                """
                val = (new_name, new_username, hashed_password, new_personal_id, new_tel_no, new_address, current_username)
                mycursor.execute(sql, val)
                mydb.commit()

                print("Personal details updated successfully.")
                break
