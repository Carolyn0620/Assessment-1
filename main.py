import car_management
import rental_management
import user_management
import db_setup
from utils import Validator
from database import Database
from functools import partial
from user import User

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
        print(f"Login successful, Welcome!\n")
        return user
    else:
        print("Login failed. Please check your username and password.")
        return None

def prompt_user_to_register(is_admin=False):
    print("\n** New Registration **\n")
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()

    name = Validator.get_valid_input("Enter name: ", Validator.is_string)
    personal_id = Validator.get_valid_input("Enter Personal ID: ", Validator.is_positive_int)
    tel_no = Validator.get_valid_input("Enter Tel. No: ", Validator.validate_tel_no)
    address = Validator.get_valid_input("Enter address: ", Validator.validate_address)

    validate_username_func = partial(Validator.validate_new_username, cursor=cursor)

    while True:
        username = Validator.get_valid_input("Enter username: ", validate_username_func)
        password = Validator.get_valid_input("Enter password: ", Validator.validate_password)

        # Set role based on is_admin flag
        role = 'admin' if is_admin else 'customer'

        user = user_management.add_user_to_db(name, personal_id, tel_no, address, username, password, role)

        if user is True:
            print(f"{'Admin' if is_admin else 'Customer'} registration successful.")
            connection.close()
            return main_menu()
        else:
            print(user)

def validate_role(user):

    if user:
        role = user.role  # Access the role attribute directly
        if role == 'customer':
            prompt_customer_function(user)
            print("Customer login successful.")
        elif role == 'admin':
            prompt_admin_function(user)
            print("Admin login successful.")
    else:
        print("Invalid username or password.")

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
                validate_role(user)
        elif option == '2':
            user = prompt_user_to_register()
            if user:
                validate_role(user.username, user.password)
        elif option == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

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
                prompt_user_to_register(is_admin=True)
            elif option == '3':
                break  # Return to the previous menu
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
    while True:
        print("\n** Customer Menu **\n")
        print("1 = View Available Car")
        print("2 = View rental history")
        print("3 = Make a car booking")
        print("4 = Logout\n")

        option = input("Select an option: ")

        if option == "1":
            car_list = view_available_car()
            if car_list:
                prompt_customer_function(user)

        elif option == '2':
            view_rental_history()

        elif option == '3':
            car_management.make_car_booking()
            prompt_customer_function(user)

        elif option == '4':
            print("Logging out. Goodbye!")
            break  # Exit the loop and log out

        else:
            print("Invalid option, please try again.")


def view_available_car():
    car_list = car_management.view_available_cars()
    return car_list

def view_rental_history():
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()

    username = input("Enter your username: ")
    sql = "SELECT * FROM rentals WHERE username = ?"
    cursor.execute(sql, (username,))
    rentals = cursor.fetchall()

    if not rentals:
        print("No rental history found for the given username.")
        return

    for rental in rentals:
        print("\nRental Details:")
        print(f"Rental ID: {rental[0]}")
        print(f"Username: {rental[1]}")
        print(f"Car ID: {rental[2]}")
        print(f"Rental Start Date: {rental[3]}")
        print(f"Rental End Date: {rental[4]}")
        print(f"Total Fee: {rental[5]}")
        print(f"Booked By: {rental[6]}")
        print(f"Email Address: {rental[7]}")
        print(f"Payment Status: {rental[8]}")
        print(f"Rental Status: {rental[8]}")
        print(f"Return Status: {rental[8]}")
   
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