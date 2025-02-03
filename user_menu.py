import hashlib
from utils import Validator

class User:
    def __init__(self, username, password, role, mycursor, mydb):
        self.username = username
        self.password = self.hash_password(password)
        self.role = role
        self.mycursor = mycursor
        self.mydb = mydb

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def save_to_db(self, name, personal_id, tel_no, address):
        sql = "INSERT INTO users (name, personal_id, tel_no, address, username, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, personal_id, tel_no, address, self.username, self.password, self.role)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(f"{self.role.capitalize()} registered successfully.")

    @classmethod
    def login(cls, username, password, mycursor, mydb):
        hashed_password = cls.hash_password(password)
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        mycursor.execute(sql, (username, hashed_password))
        user = mycursor.fetchone()

        default_admin_username = "admin"
        default_admin_password = "adminpass"
        if username == default_admin_username and password == default_admin_password:
            print("Default admin login successful.")
            admin = Admin(username, password, mycursor, mydb)
            return

        if user:
            role = user[7]  # Adjust index based on your table structure
            if role == 'customer':
                print("Customer login successful.")
                customer = Customer(username, password, mycursor, mydb)
                customer.customer_menu()
            elif role == 'admin':
                print("Admin login successful.")
                admin = Admin(username, password, mycursor, mydb)
                admin.admin_menu()
        else:
            print("Login failed. Please check your username and password.")
            return None

class Customer(User):
    def __init__(self, username, password, mycursor, mydb):
        super().__init__(username, password, "customer", mycursor, mydb)

    def customer_menu(self):
        pass

    @classmethod
    def register_customer(cls, mycursor, mydb):
        print("\n** Register New Customer **\n")
        name = Validator.get_valid_input("Enter name: ", Validator.is_string)
        personal_id = Validator.get_valid_input("Enter Personal ID: ", Validator.is_positive_int)
        tel_no = Validator.get_valid_input("Enter Tel. No: ", Validator.is_string)
        address = Validator.get_valid_input("Enter address: ", Validator.is_string)

        while True:
            username = Validator.get_valid_input("Enter username: ", Validator.is_string)
            sql = "SELECT * FROM users WHERE username = %s"
            mycursor.execute(sql, (username,))
            user = mycursor.fetchone()

            if user:
                print("Username already in use. Please choose a different username.")
            else:
                break

        password = Validator.get_valid_input("Enter password: ", Validator.is_string)
        customer = cls(username, password, mycursor, mydb)
        customer.save_to_db(name, personal_id, tel_no, address)
        print("Customer registered successfully.")
        from menus import main_menu
        main_menu(mycursor, mydb)

class Admin(User):
    def __init__(self, username, password, mycursor, mydb):
        super().__init__(username, password, "admin", mycursor, mydb)

    def admin_menu(self):
        pass
