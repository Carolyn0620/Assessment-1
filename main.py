from database import Database, create_database_schema
from customer_menu import customer_menu
from utils import Validator
import hashlib
from admin_menu import AdminMenu

class User:
    def __init__(self, username, password, role, mycursor):
        self.username = username
        self.password = self.hash_password(password)
        self.role = role
        self.mycursor = mycursor # Save cursor instance here

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def check_password(hashed_password, user_password):
        return hashed_password == hashlib.sha256(user_password.encode('utf-8')).hexdigest()

    def save_to_db(self, name, personal_id, tel_no, address):
        sql = "INSERT INTO users (name, personal_id, tel_no, address, username, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, personal_id, tel_no, address, self.username, self.password, self.role)
        mycursor.execute(sql, val)
        mydb.commit()
        print(f"{self.role.capitalize()} registered successfully.")

    @classmethod
    def login(cls, username, password):
        hashed_password = cls.hash_password(password)
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        mycursor.execute(sql, (username, hashed_password))
        user = mycursor.fetchone()

        if user:
            role = user[3]
            if role == 'admin':
                print("Admin login successful.")
                return Admin(username, password)
            elif role == 'customer':
                print("Customer login successful.")
                return Customer(username, password)
        else:
            print("Invalid username or password. Please try again.")
        return None

class Admin(User):
    DEFAULT_ADMIN_USERNAME = "admin"
    DEFAULT_ADMIN_PASSWORD = "adminpass"

    def __init__(self, username, password, mycursor):
        super().__init__(username, password, mycursor, "admin")

    def admin_menu(self):
        AdminMenu()

    @staticmethod
    def register_admin():
        print("\n** Register New Admin **\n")
        name = Validator.get_valid_input("Enter name: ", Validator.is_string)
        personal_id = Validator.get_valid_input("Enter Personal ID: ", Validator.is_positive_int)
        tel_no = Validator.get_valid_input("Enter Tel. No: ", Validator.is_string)
        address = Validator.get_valid_input("Enter address: ", Validator.is_string)
        username = Validator.get_valid_input("Enter username: ", Validator.is_string)
        password = Validator.get_valid_input("Enter password: ", Validator.is_string)
        admin = Admin(username, password)
        admin.save_to_db(name, personal_id, tel_no, address)

class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password, mycursor, "customer")

    def customer_menu(self):
        customer_menu()

    @staticmethod
    def register_customer():
        print("\n** Register New Customer **\n")
        name = Validator.get_valid_input("Enter name: ", Validator.is_string)
        personal_id = Validator.get_valid_input("Enter Personal ID: ", Validator.is_positive_int)
        tel_no = Validator.get_valid_input("Enter Tel. No: ", Validator.is_string)
        address = Validator.get_valid_input("Enter address: ", Validator.is_string)
        username = Validator.get_valid_input("Enter username: ", Validator.is_string)
        password = Validator.get_valid_input("Enter password: ", Validator.is_string)
        customer = Customer(username, password)
        customer.save_to_db(name, personal_id, tel_no, address)

class UserManager:
    def __init__(self, db_instance):
        self.db_instance = db_instance
        self.mydb = self.db_instance.get_connection()
        self.mycursor = self.db_instance.get_cursor()

    def change_username(self):
        current_username = Validator.validate_current_username(self.mycursor)

        while True:
            new_username = input("Enter your new username: ").strip()
            if Validator.validate_new_username(new_username, self.mycursor):
                sql_update_username = "UPDATE users SET username = %s WHERE username = %s"
                self.mycursor.execute(sql_update_username, (new_username, current_username))
                self.mydb.commit()
                print(f"Username changed to '{new_username}' successfully.")
                return new_username

def main_menu():
    create_database_schema()

    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit\n")
        option = input("Select an option: ")

        if option == '1':
            username = input("\nEnter username: ")
            password = input("Enter password: ")
            user = User.login(username, password)
            if user:
                if isinstance(user, Admin):
                    user.admin_menu()
                elif isinstance(user, Customer):
                    user.customer_menu()
        elif option == '2':
            print("\n1. Register as Customer\n2. Register as Admin")
            reg_option = input("Select an option: ")
            if reg_option == '1':
                Customer.register_customer(mycursor)
            elif reg_option == '2':
                Admin.register_admin(mycursor)
            else:
                print("Invalid option.")
        elif option == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    db_instance = Database()
    mydb = db_instance.get_connection()
    mycursor = db_instance.get_cursor()

    
    main_menu()
