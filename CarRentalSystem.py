import string
import mysql.connector
import hashlib
from datetime import datetime, timedelta

# Establish database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Carolyn123",
    database="python_crs"
)

mycursor = mydb.cursor()

# Function to create necessary tables
def create_database_schema():
    mycursor.execute("CREATE DATABASE IF NOT EXISTS python_crs")
    mycursor.execute("USE python_crs")
    
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role ENUM('admin', 'customer') NOT NULL
    )
    """)
    
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INT AUTO_INCREMENT PRIMARY KEY,
        make VARCHAR(255) NOT NULL,
        model VARCHAR(255) NOT NULL,
        plate_number VARCHAR(255) NOT NULL,
        color VARCHAR(255) NOT NULL,
        seats INT NOT NULL,
        rate_per_hour FLOAT NOT NULL,
        rate_per_day FLOAT NOT NULL,
        year INT NOT NULL,
        mileage INT NOT NULL,
        available_now TINYINT(1) NOT NULL,
        min_rent_period INT NOT NULL,
        max_rent_period INT NOT NULL
    )
""")
    
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        car_id INT NOT NULL,
        rental_start DATE NOT NULL,
        rental_end DATE NOT NULL,
        total_fee FLOAT NOT NULL,
        status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (car_id) REFERENCES cars(id)
    )
    """)
    
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rental_id INT NOT NULL,
        amount FLOAT NOT NULL,
        payment_method ENUM('Cash', 'Cheque') NOT NULL,
        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (rental_id) REFERENCES rentals(id)
    )
    """)
    
    mydb.commit()

create_database_schema()

# Function to register a new user
def register_user(username, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    val = (username, hashed_password, role)
    mycursor.execute(sql, val)
    mydb.commit()
    print("User registered successfully.")

# Function to login a user
def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username, hashed_password)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    log_query(sql, val)
    return user

# Function to log queries
def log_query(sql, val=None):
    log_sql = "INSERT INTO query_log (query, query_values) VALUES (%s, %s)"
    log_val = (sql, str(val) if val else 'NULL')
    mycursor.execute(log_sql, log_val)
    mydb.commit()

# Function to update customer payment
def update_payment(rental_id, amount, payment_method):
    sql = "INSERT INTO payments (rental_id, amount, payment_method) VALUES (%s, %s, %s)"
    val = (rental_id, amount, payment_method)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Payment updated successfully.")

# Function to return a rented car
def return_rented_car(rental_id):
    sql = "DELETE FROM rentals WHERE id = %s"
    mycursor.execute(sql, (rental_id,))
    mydb.commit()
    print("Car returned successfully.")

# Function to display all cars
def display_cars():
    sql = "SELECT * FROM cars"
    mycursor.execute(sql)
    cars = mycursor.fetchall()
    for car in cars:
        print(car)

# Function to search for a car
def search_car(make, model):
    sql = "SELECT * FROM cars WHERE make = %s AND model = %s"
    mycursor.execute(sql, (make, model))
    results = mycursor.fetchall()
    for car in results:
        print(car)

# Function to book a car
def book_car(user_id, car_id, rental_start, rental_end, total_fee):
    sql = "INSERT INTO rentals (user_id, car_id, rental_start, rental_end, total_fee) VALUES (%s, %s, %s, %s, %s)"
    val = (user_id, car_id, rental_start, rental_end, total_fee)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Car booked successfully.")

# Function to calculate rental fee
def calculate_rental_fee(car_id, rental_start, rental_end):
    sql = "SELECT * FROM cars WHERE id = %s"
    mycursor.execute(sql, (car_id,))
    car = mycursor.fetchone()
    
    start_date = datetime.strptime(rental_start, "%Y-%m-%d")
    end_date = datetime.strptime(rental_end, "%Y-%m-%d")
    rental_days = (end_date - start_date).days + 1  # Include the last day
    
    daily_rate = 50  # Assume a daily rate of 50 units
    total_fee = rental_days * daily_rate
    
    print(f"Total rental fee for {rental_days} days is: {total_fee}")
    return total_fee


# Prompt user for input and validate it    
def get_valid_input(prompt, validation_func):
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        else:
            print("Invalid input. Please try again.")

def is_positive_int(value):
    return value.isdigit() and int(value) > 0

def is_string(value):
    return isinstance(value, str) and value.strip() != ""

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Admin menu function
def admin_menu():
    while True:
        print("\n** Admin Menu **\n")
        print("1 = Add Car")
        print("2 = Modify Car")
        print("3 = Display Car")
        print("4 = Search Car")
        print("5 = Update Customer Payment (Cash/Cheque)")
        print("6 = Return Rented Car")
        print("7 = Return to Previous Menu\n")
        
        option = input("Select an option: ")
        
        if option == '1':
            while True:
                print("\n** Add Car Data Entry **\n")
                make = get_valid_input("Enter car make: ", is_string)
                model = get_valid_input("Enter car model: ", is_string)
                plate_number = input("Enter car plate number: ")
                color = get_valid_input("Enter car colour: ", is_string)
                seats = int(get_valid_input("Enter number of seats: ", is_positive_int))
                rate_per_hour = float(get_valid_input("Enter rate per hour: ", is_float))
                rate_per_day = float(get_valid_input("Enter rate per day: ", is_float))
                year = int(get_valid_input("Enter car year: ", is_positive_int))
                mileage = int(get_valid_input("Enter car mileage: ", is_positive_int))
                available_now = int(get_valid_input("Is the car available now? (1 = Yes, 0 = No): ", lambda x: x in ['0', '1']))
                min_rent_period = int(get_valid_input("Enter minimum rent period (day): ", is_positive_int))
                max_rent_period = int(get_valid_input("Enter maximum rent period (day): ", is_positive_int))
                
                # Confirm data entry
                print("\nThese are the details of the car.\n")
                print(f"Make: {make}")
                print(f"Model: {model}")
                print(f"Plate Number: {plate_number}")
                print(f"Car Colour: {color}")
                print(f"Number of Seats: {seats}")
                print(f"Rate Per Hour: {rate_per_hour}")
                print(f"Rate Per Day: {rate_per_day}")
                print(f"Year: {year}")
                print(f"Mileage: {mileage}")
                print(f"Available Now: {available_now}")
                print(f"Minimum Rent Period: {min_rent_period}")
                print(f"Maximum Rent Period: {max_rent_period}")

                confirm = input("Are you sure you want to save the record? (Y/N): ")
                if confirm.lower() == 'y':
                    sql = """
                    INSERT INTO cars (
                        make, model, plate_number, color, seats, rate_per_hour, 
                        rate_per_day, year, mileage, available_now,
                        min_rent_period, max_rent_period
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    val = (
                        make, model, plate_number, color, seats, rate_per_hour, 
                        rate_per_day, year, mileage, available_now,
                        min_rent_period, max_rent_period
                    )
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("Car added successfully.")    
                    break
            
                else:
                    reenter = input("Car record not saved. Re-enter the details? (Y/N): ")
                    if reenter.lower() == 'y':
                        continue  # This will loop back to re-enter car details
                    else:
                        break
            
        elif option == '2':
            car_id = int(input("\nEnter the car ID to modify: "))
            print("\n** Modify Car Details **\n")
            make = get_valid_input("Enter new car make: ", is_string)
            model = get_valid_input("Enter new car model: ", is_string)
            plate_number = input("Enter new car plate number: ")
            color = get_valid_input("Enter new car colour: ", is_string)
            seats = int(get_valid_input("Enter new number of seats: ", is_positive_int))
            rate_per_hour = float(get_valid_input("Enter new rate per hour: ", is_float))
            rate_per_day = float(get_valid_input("Enter new rate per day: ", is_float))
            year = int(get_valid_input("Enter new car year: ", is_positive_int))
            mileage = int(get_valid_input("Enter new car mileage: ", is_positive_int))
            available_now = int(get_valid_input("Is the car available now? (1 = Yes, 0 = No): ", lambda x: x in ['0', '1']))
            min_rent_period = int(get_valid_input("Enter new minimum rent period (day): ", is_positive_int))
            max_rent_period = int(get_valid_input("Enter new maximum rent period (day): ", is_positive_int))
            
            sql = """
            UPDATE cars SET make=%s, model=%s, plate_number=%s, color=%s, seats=%s, rate_per_hour=%s, 
            rate_per_day=%s, year=%s, mileage=%s, available_now=%s, min_rent_period=%s, 
            max_rent_period=%s WHERE id=%s
            """
            val = (
                make, model, plate_number, color, seats, rate_per_hour, 
                rate_per_day, year, mileage, available_now,
                min_rent_period, max_rent_period, car_id
            )
            mycursor.execute(sql, val)
            mydb.commit()
            print("Car details updated successfully.")

        elif option == '3':
            display_cars()
        elif option == '4':
            make = input("Enter car make to search: ")
            model = input("Enter car model to search: ")
            search_car(make, model)
        elif option == '5':
            rental_id = int(input("Enter rental ID: "))
            amount = float(input("Enter payment amount: "))
            payment_method = input("Enter payment method (Cash/Cheque): ")
            update_payment(rental_id, amount, payment_method)
        elif option == '6':
            rental_id = int(input("Enter rental ID to return car: "))
            return_rented_car(rental_id)
        elif option == '7':
            break # Exit the loop and return to the previous menu
        else:
            print("Invalid option, please try again.")



# Customer menu function
def customer_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Check login credentials (implement your own logic)
    sql = "SELECT * FROM customers WHERE username = %s AND password = %s"
    mycursor.execute(sql, (username, password))
    result = mycursor.fetchone()
    
    if result:
        print("Login successful.")
        return result[0]  # Assuming the first column is the customer ID
    else:
        print("Invalid login credentials. Please try again.")
        return None

def modify_personal_details(customer_id):
    print("Modify Personal Details")
    
    new_username = input("Enter new username: ")
    new_password = input("Enter new password: ")
    new_email = input("Enter new email: ")
    
    sql = "UPDATE customers SET username = %s, password = %s, email = %s WHERE id = %s"
    mycursor.execute(sql, (new_username, new_password, new_email, customer_id))
    mydb.commit()
    
    print("Personal details updated successfully.")

def view_rental_history(customer_id):
    sql = "SELECT * FROM rentals WHERE customer_id = %s"
    mycursor.execute(sql, (customer_id,))
    rentals = mycursor.fetchall()
    for rental in rentals:
        print(rental)

def view_details_of_booked_car(customer_id):
    sql = """
    SELECT cars.*
    FROM rentals
    JOIN cars ON rentals.car_id = cars.id
    WHERE rentals.customer_id = %s AND rentals.rental_end >= CURDATE()
    """
    mycursor.execute(sql, (customer_id,))
    cars = mycursor.fetchall()
    for car in cars:
        print(car)

def make_car_booking(user_id):
    car_id = int(input("Enter car ID to book: "))
    rental_start = input("Enter rental start date (YYYY-MM-DD): ")
    rental_end = input("Enter rental end date (YYYY-MM-DD): ")
    total_fee = calculate_rental_fee(car_id, rental_start, rental_end)
    book_car(user_id, car_id, rental_start, rental_end, total_fee)

def make_payment(user_id):
    # Implement make payment functionality
    pass

# Customer menu function
def customer_menu(user_id):
    while True:
        print("\n** Customer Menu **\n")
        print("1 = Customer login")
        print("2 = Modify personal details")
        print("3 = View rental history")
        print("4 = View details of booked car")
        print("5 = Make a car booking")
        print("6 = Make payment")
        print("7 = Logout\n")
        
        option = input("Select an option: ")
        
        if option == '1':
            user_id = customer_login()
        elif option == '2':
            if user_id:
                modify_personal_details(user_id)
            else:
                print("You need to log in first.")
        elif option == '3':
            if user_id:
                view_rental_history(user_id)
            else:
                print("You need to log in first.")
        elif option == '4':
            if user_id:
                view_details_of_booked_car(user_id)
            else:
                print("You need to log in first.")
        elif option == '5':
            if user_id:
                make_car_booking(user_id)
            else:
                print("You need to log in first.")
        elif option == '6':
            if user_id:
                make_payment(user_id)
            else:
                print("You need to log in first.")
        elif option == '7':
            break
        else:
            print("Invalid option, please try again.")

def display_cars():
    while True:
        print("\nDisplay Specific Records of:")
        print("1 = Cars Rented Out")
        print("2 = Cars Available for Rent")
        print("3 = Customer Booking For Cars")
        print("4 = Customer Payment for a Specific Time Duration")
        print("5 = Customer Records")
        print("6 = Return to Previous Menu\n")
        
        option = input("Select an option: ")
        
        if option == '1':
            display_cars_rented_out()
        elif option == '2':
            display_cars_available_for_rent()
        elif option == '3':
            display_customer_booking_for_cars()
        elif option == '4':
            display_customer_payment_for_specific_time_duration()
        elif option == '5':
            display_customer_records()
        elif option == '6':
            break
        else:
            print("Invalid option, please try again.")

def display_cars_rented_out():
    sql = "SELECT * FROM rentals WHERE rental_end >= CURDATE()"
    mycursor.execute(sql)
    rentals = mycursor.fetchall()
    for rental in rentals:
        print(rental)

def display_cars_available_for_rent():
    sql = "SELECT * FROM cars WHERE available_now = 1"
    mycursor.execute(sql)
    cars = mycursor.fetchall()
    for car in cars:
        print(car)

def display_customer_booking_for_cars():
    sql = "SELECT * FROM rentals"
    mycursor.execute(sql)
    rentals = mycursor.fetchall()
    for rental in rentals:
        print(rental)

def display_customer_payment_for_specific_time_duration():
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    sql = "SELECT * FROM payments WHERE payment_date BETWEEN %s AND %s"
    val = (start_date, end_date)
    mycursor.execute(sql, val)
    payments = mycursor.fetchall()
    for payment in payments:
        print(payment)

def display_customer_records():
    sql = "SELECT * FROM users"
    mycursor.execute(sql)
    users = mycursor.fetchall()
    for user in users:
        print(user)

                  
# Function to manage rental bookings
def manage_rentals():
    while True:
        print("\n** Manage Rentals **\n")
        print("1 = View All Rentals")
        print("2 = Approve Rental")
        print("3 = Reject Rental")
        print("4 = Return to Previous Menu\n")
        
        option = input("Select an option: ")
        
        if option == '1':
            sql = "SELECT * FROM rentals"
            mycursor.execute(sql)
            rentals = mycursor.fetchall()
            for rental in rentals:
                print(rental)
        elif option == '2':
            rental_id = int(input("Enter rental ID to approve: "))
            sql = "UPDATE rentals SET status = 'approved' WHERE id = %s"
            mycursor.execute(sql, (rental_id,))
            mydb.commit()
            print("Rental approved successfully.")
        elif option == '3':
            rental_id = int(input("Enter rental ID to reject: "))
            sql = "UPDATE rentals SET status = 'rejected' WHERE id = %s"
            mycursor.execute(sql, (rental_id,))
            mydb.commit()
            print("Rental rejected successfully.")
        elif option == '4':
            break
        else:
            print("Invalid option, please try again.")

# Function to register admin user
def register_admin_user():
    username = input("Enter new admin username: ")
    password = input("Enter new admin password: ")
    
    sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    mycursor.execute(sql, (username, password, 'admin'))
    mydb.commit()
    
    print(f"Admin user {username} registered successfully.")

# Main Manu
def main_menu():
    while True:
        print("\n** MyRide Car Rental **\n")
        print("1 = Admin User")
        print("2 = Member Customer")
        print("3 = Non-Member Customer")
        print("4 = Exit\n")
        
        option = input("Select an option: ")
        
        if option == '1':
            print("1 = Login")
            print("2 = New Register\n")
            
            admin_option = input("Select an option: ")
            
            if admin_option == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = login_user(username, password)
                if user and user[3] == 'admin':
                    print(f"Welcome Admin {user[1]}!")
                    admin_menu()
                else:
                    print("Invalid credentials or not an admin. Please try again.")
            elif admin_option == '2':
                register_admin_user()
            else:
                print("Invalid option. Please try again.")
        
        elif option == '2' or option == '3':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = login_user(username, password)
            if user:
                print(f"Welcome {user[1]}!")
                customer_menu(user[0])  # Assuming the customer_menu function requires the user ID
            else:
                print("Invalid credentials. Please try again.")
        
        elif option == '4':
            print("Exiting...")
            #close_connection()
            break
        
        else:
            print("Invalid option, please try again.")


# Run the application
main_menu()