import car_management
import rental_management
import user_management
from utils import Validator
from database import Database
from user import User
import db_setup

def prompt_user_to_login():
    print("\n** Login to your account. **\n")
    username = input("Enter username: ")
    password = input("Enter password: ")

    default_admin_username = "admin"
    default_admin_password = "adminpass"
    if username == default_admin_username and password == default_admin_password:
        print("Default admin login successful.")
        return prompt_default_admin_funtion()
    
    user = user_management.get_user_from_db(username, password)

    if user:
        print(f"Login successful, Welcome!")
        return user
    else:
        print("Login failed. Please check your username and password.")
        return None
    
def prompt_user_to_register(role='customer'):
    print("\n** New Registration **\n")
    name = Validator.get_valid_input("Enter name: ", Validator.is_string)
    personal_id = Validator.get_valid_input("Enter Personal ID: ", Validator.is_positive_int)
    tel_no = Validator.get_valid_input("Enter Tel. No: ", Validator.validate_tel_no)
    address = Validator.get_valid_input("Enter address: ", Validator.validate_address)

    while True:
        username = Validator.get_valid_input("Enter username: ", Validator.validate_username)
        password = Validator.get_valid_input("Enter password: ", Validator.validate_password)
        role = 'customer'  # Default role is customer

        user = user_management.add_user_to_db(name, personal_id, tel_no, address, username, password, role)

        if user is True:
            print("Registration successful.")
            return main_menu()
        else:
            print(user)  

def prompt_admin_to_register(role='admin'):
    print("\n** Admin New Registration **\n")
    name = Validator.get_valid_input("Enter name: ", Validator.is_string)
    personal_id = Validator.get_valid_input("Enter Personal ID: ", Validator.is_positive_int)
    tel_no = Validator.get_valid_input("Enter Tel. No: ", Validator.validate_tel_no)
    address = Validator.get_valid_input("Enter address: ", Validator.validate_address)

    while True:
        username = Validator.get_valid_input("Enter username: ", Validator.validate_username)
        password = Validator.get_valid_input("Enter password: ", Validator.validate_password)
        role = 'admin'  # Default role is admin

        user = user_management.add_user_to_db(name, personal_id, tel_no, address, username, password, role)

        if user is True:
            print("Registration successful.")
            return main_menu()
        else:
            print(user)
 
import hashlib
import sqlite3

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Database connection
def connect_to_db():
    return sqlite3.connect('your_database.db')

# Functions to prompt user actions based on role
def prompt_customer_function(user):
    # Customer-specific functionality
    print(f"Welcome, {user[1]}! You are logged in as a customer.")

def prompt_admin_function(user):
    # Admin-specific functionality
    print(f"Welcome, {user[1]}! You are logged in as an admin.")


def validate_role(username, password):
    connection = connect_to_db()
    cursor = connection.cursor()

    # Hash the password
    hashed_password = User.hash_password(password)
    print("Hashed password:", hashed_password)  # Debug: print hashed password

    # Ensure correct values are being passed
    print("Username:", username)  # Debug: print username
    print("Password:", password)  # Debug: print plain-text password

    sql = "SELECT * FROM users WHERE username = ? AND password = ?"
    print("Executing SQL query:", sql)
    print("With parameters:", (username, hashed_password))

    cursor.execute(sql, (username, hashed_password))
    user = cursor.fetchone()
    print("SQL query executed.")  # Debug: indicate query execution

    connection.close()
    print("Connection closed.")  # Debug: indicate connection closed

    if user:
        print("User data:", user)  # Debug: print the user data
        role = user[8]  # Adjust the index based on your table structure
        if role == 'customer':
            prompt_customer_function(user)
            print("Customer login successful.")
        elif role == 'admin':
            prompt_admin_function(user)
            print("Admin login successful.")
    else:
        print("Invalid username or password.")



# def validate_role(username, password):
#     connection = connect_to_db()
#     cursor = connection.cursor()

#     # Call the static method to hash the password
#     hashed_password = User.hash_password(password)  

#     sql = "SELECT * FROM users WHERE username = ? AND password = ?"
#     cursor.execute(sql, (username, hashed_password))
#     user = cursor.fetchone()

#     connection.close()

#     if user:
#         print("User data:", user)  # Debug: print the user data
#         role = user[8]  # Adjust the index based on your table structure
#         if role == 'customer':
#             prompt_customer_function()
#             print("Customer login successful.")
#         elif role == 'admin':
#             prompt_admin_function()
#             print("Admin login successful.")
#     else:
#         print("Invalid username or password.")


def main_menu():
    db_setup.create_tables()

    while True:
        print("\n** Welcome to Aloha Car Rental Service **\n")
        print("--- Main Menu ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit\n")
        option = input("Select an option: ")

        if option == '1':
            user = prompt_user_to_login()
            if user:
                validate_role(user.username, user.password)
        elif option == '2':
            user = prompt_user_to_register()
            if user:
                validate_role(user.username, user.passworder)
        elif option == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

def prompt_admin_function(user_id):
    # Prompt admin to select a function
    print("Please select a function: \n(1) Rental Management \n(2) Car Management\n")
    choice = input("Number: ")

    if choice == "1":
        prompt_admin_rental_management(user_id)
        prompt_admin_function(user_id)
        return
    elif choice == "2":
        prompt_admin_car_management(user_id)
        prompt_admin_function(user_id)
        return
    else:
        print("Invalid selection. Please enter '1' or '2'.")
        prompt_admin_function(user_id)  # Prompt the user again"""

def prompt_default_admin_funtion():
    
    def __init__(self, username, password, mycursor, mydb):
        super().__init__(username, password, "admin", mycursor, mydb)
        self.mydb = mydb
        self.mycursor = mycursor
            
    while True:
            print("\n** Default Admin Menu **\n")
            print("1. Update Admin Details")
            print("2. Register New Admin")
            print("3. Main Menu\n")
            option = input("Select an option: ")

            if option == '1':
                print("\n** Update Admin Details **\n")
                user_management.modify_personal_details()
            elif option == '2':
                register_new_admin()
            elif option == '3':
                break  # Return to the previous menu
            else:
                print("Invalid option, please try again.")

def register_new_admin():
    prompt_admin_to_register(role='admin')


def prompt_admin_rental_management(user_id):
    # Prompt admin to select a function from rental management
    print("Please select a function: \n(1) View Pending Booking \n(2) Update Booking Status "
          "\n(3) Back to Admin Function Menu")
    choice = input("Number: ")

    if choice == "1":
        view_pending_bookings()
        prompt_admin_function(user_id)
        return
    elif choice == "2":
        update_booking_status()
        prompt_admin_function(user_id)
        return
    elif choice == "3":
        prompt_admin_function(user_id)
        return
    else:
        print("Invalid selection. Please enter '1' or '2' or '3'.")
        prompt_admin_rental_management(user_id)  # Prompt the user again"""


def prompt_add_car_details(valid):
    # Prompt admin to add new cars
    print("Please enter car's detail:")
    make = input("Make: ")
    model = input("Model: ")
    year = input("Year: ")
    mileage = input("Mileage: ")
    min_rent_period = 1
    max_rent_period = 7

    valid = car_management.add_car_to_db(make, model, year, mileage, min_rent_period, max_rent_period)
    return valid


def prompt_delete_car_details():
    # Prompt admin to delete car
    print("Please enter car's ID:")
    car_id = input("Car's ID: ")
    print(car_management.delete_car_from_db(car_id))
    return None


def prompt_update_car_details():
    # Prompt admin to add new cars
    print("Please enter car's ID:")
    car_id = input("Car's ID: ")
    mileage = input("Mileage: ")
    availability = input("Availability: ")
    print(car_management.update_car_to_db(car_id, mileage, availability))


def prompt_admin_car_management(user_id):
    # Prompt admin to select a function from car management
    print("Please select a function: \n(1) Add Car \n(2) Delete A Car \n(3) Update Car Mileage "
          "\n(4) Back to Admin Function Menu")
    choice = input("Number: ")

    if choice == "1":
        valid = True
        validity = prompt_add_car_details(valid)
        if validity:
            prompt_admin_function(user_id)
        else:
            prompt_admin_car_management(user_id)
        return
    elif choice == "2":
        prompt_delete_car_details()
        prompt_admin_function(user_id)
        return
    elif choice == "3":
        prompt_update_car_details()
        prompt_admin_function(user_id)
        return
    elif choice == "4":
        prompt_admin_function(user_id)
        return
    else:
        print("Invalid selection. Please enter '1' or '2' or '3' or '4'.")
        prompt_admin_car_management(user_id)  # Prompt the user again"""


def view_pending_bookings():
    rental_management.get_all_pending_bookings()


def update_booking_status():
    booking_id = input("Please enter Booking ID:")
    status = input("Please enter Booking Status: ")

    rental_management.update_booking_status(booking_id, status.strip().lower())


def prompt_customer_function(user):
    print("Please choose an option: \n(1) View Available Cars \n(2) Book Car\n")
    choice = input("Number: ")

    if choice == "1":
        car_list = view_available_car()

        if car_list:
            prompt_customer_function(user)

    elif choice == "2":
        prompt_book_car(user.get_user_id())
        prompt_customer_function(user)

    else:
        print("Invalid selection. Please enter '1' or '2'.")
        prompt_customer_function(user)  # Prompt the user again


def view_available_car():
    car_list = car_management.view_available_cars()
    return car_list


def prompt_book_car(user_id):
    # Prompt customer to book car
    print("Please enter your information below:")
    car_id = input("Car ID: ")
    start_date = input("Start Date(YYYY-MM-DD): ")
    end_date = input("End Date (YYYY-MM-DD): ")
    daily_rate = input("Daily Rate: ")
    booking_detail = rental_management.book_car(user_id, car_id, start_date, end_date, daily_rate, "pending")
    return booking_detail

if __name__ == "__main__":
    main_menu()