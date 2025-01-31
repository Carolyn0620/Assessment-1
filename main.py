import hashlib
from database import create_database_schema, mycursor, mydb
from admin_menu import admin_menu
from customer_menu import customer_menu, modify_personal_details
from utils import get_valid_input, is_positive_int, is_string

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = self.hash_password(password)
        self.role = role

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
    
    def __init__(self, username, password):
        super().__init__(username, password, "admin")
    
    def admin_menu(self):
        admin_menu()
    
    @staticmethod
    def register_admin():
        print("\n** Register New Admin **\n")
        name = get_valid_input("Enter name: ", is_string)
        personal_id = get_valid_input("Enter Personal ID: ", is_positive_int)
        tel_no = get_valid_input("Enter Tel. No: ", is_string)
        address = get_valid_input("Enter address: ", is_string)
        username = get_valid_input("Enter username: ", is_string)
        password = get_valid_input("Enter password: ", is_string)
        admin = Admin(username, password)
        admin.save_to_db(name, personal_id, tel_no, address)

class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password, "customer")
    
    def customer_menu(self):
        customer_menu()
    
    @staticmethod
    def register_customer():
        print("\n** Register New Customer **\n")
        name = get_valid_input("Enter name: ", is_string)
        personal_id = get_valid_input("Enter Personal ID: ", is_positive_int)
        tel_no = get_valid_input("Enter Tel. No: ", is_string)
        address = get_valid_input("Enter address: ", is_string)
        username = get_valid_input("Enter username: ", is_string)
        password = get_valid_input("Enter password: ", is_string)
        customer = Customer(username, password)
        customer.save_to_db(name, personal_id, tel_no, address)

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
                Customer.register_customer()
            elif reg_option == '2':
                Admin.register_admin()
            else:
                print("Invalid option.")
        elif option == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main_menu()
