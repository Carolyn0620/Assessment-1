import car_management
import rental_management
import user_management
import db_setup
from utils import Validator
from database import Database
from functools import partial
from user import User
from datetime import datetime


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
    print("\n** Admin Menu **\n")
    print("1. Rental Management")
    print("2. Car Management")
    print("3. Return to Previous Menu")
    option = input("Select an option: ")

    if option == "1":
        prompt_admin_rental_management(user_id)
        prompt_admin_function(user_id)
        return
    elif option == "2":
        prompt_admin_car_management(user_id)
        prompt_admin_function(user_id)
        return
    elif option == '3':
        main_menu()
    else:
        print("Invalid option, please try again.")

def prompt_admin_rental_management(user_id):
    # Prompt admin to select a function from rental management
    print("\n** Rental Management **\n")
    print("1. Update Customer Payment")
    print("2. Return Rented Car")
    print("3. Manage Rental Requests")
    print("4. Return to Previous Menu\n")
    option = input("Select an option: ")

    if option == "1":
        prompt_update_payment_status()
        prompt_admin_rental_management(user_id)
        return
    elif option == "2":
        prompt_return_rented_car()
        prompt_admin_rental_management(user_id)
        return
    elif option == "3":
        prompt_manage_rental_requests()
        prompt_admin_rental_management(user_id)
        return
    elif option == "4":
        prompt_admin_function(user_id)
        return
    else:
        print("Invalid selection. Please enter '1' or '2' or '3'.")
        prompt_admin_rental_management(user_id)  # Prompt the user again"""


def prompt_update_payment_status():
    rental_management.display_rentals_table()
    # Prompt admin to update payment status
    id = input("Enter the rental ID: ")
    payment_status = input("Enter payment status (Paid, Unpaid): ")

    rental_management.update_payment_status_to_db(id, payment_status)

def prompt_update_car_details():
    car_management.view_available_cars()
    car_id = input("Enter the car ID: ")
    mileage = input("Enter car mileage: ")
    available_now = input("Is the car available now? (Y = Yes, N = No): ")
    car_management.update_car_to_db(car_id, mileage, available_now)

def prompt_add_car_details(valid):
    car_management.view_available_cars()
    print("\n** Add Car Data Entry **\n")
    make = Validator.get_valid_input("Enter car make: ", Validator.is_string)
    model = Validator.get_valid_input("Enter car model: ", Validator.is_string)
    plate_number = input("Enter car plate number: ")
    color = Validator.get_valid_input("Enter car colour: ", Validator.is_string)
    seats = int(Validator.get_valid_input("Enter number of seats: ", Validator.is_positive_int))
    rate_per_hour = float(Validator.get_valid_input("Enter rate per hour: ", Validator.is_float))
    rate_per_day = float(Validator.get_valid_input("Enter rate per day: ", Validator.is_float))
    year = int(Validator.get_valid_input("Enter car year: ", Validator.is_positive_int))
    mileage = int(Validator.get_valid_input("Enter car mileage: ", Validator.is_positive_int))
    available_now = Validator.get_valid_input("Is the car available now? (Y = Yes, N = No): ", lambda x: x.lower() in ['y', 'n']).lower()
    min_rent_period = int(Validator.get_valid_input("Enter minimum rent period (day): ", Validator.is_positive_int))
    max_rent_period = int(Validator.get_valid_input("Enter maximum rent period (day): ", Validator.is_positive_int))
                
    valid = car_management.add_car_to_db(make, model, plate_number, color, seats, rate_per_hour, rate_per_day, year, mileage, available_now, min_rent_period, max_rent_period)
    return valid

def prompt_delete_car_details():
    car_management.view_available_cars()
    # Prompt admin to delete car
    car_id = input("Enter Car's ID to delete: ")
    print(car_management.delete_car_from_db(car_id))
    return None

def prompt_admin_car_management(user_id):
# Prompt admin to select a function from car management
    print("\n** Car Management **\n")
    print("1 = Add Car")
    print("2 = Delete Car")
    print("3 = Update Car")
    print("4 = Return to Previous Menu\n")
            
    option = input("Select an option: ")

    if option == "1":
        valid = True
        validity = prompt_add_car_details(valid)
        if validity:
            prompt_admin_function(user_id)
        else:
            prompt_admin_car_management(user_id)
        return
    elif option == "2":
        prompt_delete_car_details()
        prompt_admin_function(user_id)
        return
    elif option == "3":
        prompt_update_car_details()
        prompt_admin_function(user_id)
        return
    elif option == "4":
        prompt_admin_function(user_id)
        return
    else:
        print("Invalid selection. Please enter '1' or '2' or '3' or '4'.")
        prompt_admin_car_management(user_id)  # Prompt the user again"""

def prompt_manage_rental_requests():
    while True:
        rental_management.view_rentals_requests()
        request_id = input("Enter the Request ID to approve/reject (or 'Q' to quit): ")
        
        if request_id.strip().lower() == 'q':
            break

        action = input("Enter 'A' to approve or 'R' to reject the request: ").strip().lower()
        if action == 'a':
            rental_management.update_rental_status(request_id, 'approved')
        elif action == 'r':
            rental_management.update_rental_status(request_id, 'rejected')
        else:
            print("Invalid action. Please enter 'A' to approve or 'R' to reject.")

def view_pending_bookings():
    rental_management.get_all_pending_bookings()


def prompt_return_rented_car():
    rental_management.display_rentals_table()
    car_id = input("Enter the Returned car ID: ")
    while True:
        return_status = input("Has the car been returned? (Y/N): ").lower()
        if return_status in ['y', 'n']:
            break
        print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")
    
    # Update the return status in the rentals table based on the input
    if return_status == 'y':
        rental_management.update_returned_car_to_db(car_id, "returned")
    else:
        rental_management.update_returned_car_to_db(car_id, "pending")


def prompt_customer_function(user):
    while True:
        print("\n** Customer Menu **\n")
        print("1 = View Available Car")
        print("2 = View rental history")
        print("3 = Make a car booking")
        print("4 = Logout\n")

        option = input("Select an option: ")

        if option == "1":
            car_list = car_management.view_available_cars()
            if car_list:
                prompt_customer_function(user)

        elif option == '2':
            view_rental_history()

        elif option == '3':
            prompt_book_car()
            prompt_customer_function(user)

        elif option == '4':
            print("Logging out. Goodbye!")
            break  # Exit the loop and log out

        else:
            print("Invalid option, please try again.")


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
        print(f"Payment Status: {rental[10]}")
        print(f"Rental Status: {rental[8]}")
        print(f"Return Status: {rental[9]}")
   
def prompt_book_car():
    # Prompt customer to book car
    while True:
        username = input("Enter your username: ")
        if username.strip():  # Check if the input is not empty
            break
        print("Invalid input. Please enter a valid username.")
    
    # Validate car ID
    while True:
        try:
            car_id = int(input("Enter car ID to book: "))
            break
        except ValueError:
            print("Invalid input. Car ID must be a number. Please try again.")

    # Validate rental start date
    while True:
        rental_start = input("Enter rental start date (YYYY-MM-DD): ")
        try:
            datetime.strptime(rental_start, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    # Validate rental end date
    while True:
        rental_end = input("Enter rental end date (YYYY-MM-DD): ")
        try:
            datetime.strptime(rental_end, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    # Validate booked by
    while True:
        booked_by = input("Enter the name of the person booking the car: ")
        if booked_by.strip():  # Check if the input is not empty
            break
        print("Invalid input. Please enter a valid name.")

    # Validate email address
    while True:
        email_address = input("Enter email address: ")
        if email_address.strip():  # Check if the input is not empty
            break
        print("Invalid input. Please enter a valid email address.")

    total_fee = rental_management.calculate_rental_fee(car_id, rental_start, rental_end)
    rental_management.book_car(username, car_id, rental_start, rental_end, total_fee, booked_by, email_address)

if __name__ == "__main__":
    main_menu()