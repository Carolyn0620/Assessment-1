import mysql.connector  # Import the MySQL connector library
import hashlib  # Import the hashlib library for hashing passwords
from datetime import datetime  # Import the datetime module for date manipulation

# Establish the connection to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Carolyn123",
    database="python_crs"
)

mycursor = mydb.cursor()  # Create a cursor object to interact with the database

# Fetch and print all users from the 'users' table
mycursor.execute("SELECT * FROM users")
users = mycursor.fetchall()
for user in users:
    print(user)

# Function to insert a user into the 'users' table
def insert_user(username, password, role):
    """
    Insert a new user into the users table.
    
    Args:
    username (str): The username of the user.
    password (str): The password of the user.
    role (str): The role of the user ('admin' or 'customer').
    """
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
    sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"  # SQL query
    val = (username, hashed_password, role)  # Values to insert
    mycursor.execute(sql, val)  # Execute the query
    mydb.commit()  # Commit the transaction
    print(mycursor.rowcount, "record inserted.")  # Print confirmation

# Insert sample users
insert_user('admin_user', 'admin_password', 'admin')
insert_user('customer_user', 'customer_password', 'customer')

# Function to get all available cars
def get_available_cars():
    """
    Retrieve and print all available cars from the cars table.
    """
    sql = "SELECT * FROM cars WHERE available_now = TRUE"  # SQL query
    mycursor.execute(sql)  # Execute the query
    result = mycursor.fetchall()  # Fetch all results
    for car in result:
        print(car)  # Print each available car

# Get and print all available cars
get_available_cars()

# Function to check if a record exists in a specific table
def record_exists(table, column, value):
    """
    Check if a record exists in the specified table.
    
    Args:
    table (str): The name of the table.
    column (str): The column to check.
    value (any): The value to look for in the column.
    
    Returns:
    bool: True if the record exists, False otherwise.
    """
    sql = f"SELECT 1 FROM {table} WHERE {column} = %s"  # SQL query
    mycursor.execute(sql, (value,))  # Execute the query with the value
    return mycursor.fetchone() is not None  # Return whether a record was found

# Function to book a car
def book_car(user_id, car_id, rental_start, rental_end, total_fee):
    """
    Book a car for a user.
    
    Args:
    user_id (int): The ID of the user.
    car_id (int): The ID of the car.
    rental_start (datetime): The start date of the rental.
    rental_end (datetime): The end date of the rental.
    total_fee (float): The total fee for the rental.
    """
    if not record_exists("cars", "id", car_id):
        print("Error: car_id does not exist in cars table.")
        return
    if not record_exists("users", "id", user_id):
        print("Error: user_id does not exist in users table.")
        return

    sql = """
    INSERT INTO rentals (user_id, car_id, rental_start, rental_end, total_fee)
    VALUES (%s, %s, %s, %s, %s)
    """  # SQL query
    val = (user_id, car_id, rental_start, rental_end, total_fee)  # Values to insert
    mycursor.execute(sql, val)  # Execute the query
    mydb.commit()  # Commit the transaction
    print(mycursor.rowcount, "record inserted.")  # Print confirmation

# Example booking
book_car(1, 2, datetime(2025, 2, 1), datetime(2025, 2, 10), 150.00)

# Main Menu function
def main_menu():
    """
    Display the main menu for the car rental system and handle user choices.
    """
    while True:
        print("** MyRide Car Rental**")
        print("\nPlease select an option:")
        print("1 = Admin User")
        print("2 = Member Customer")
        print("3 = Non-Member Customer")
        print("4 = Exit")
        
        option = input("Enter your choice: ")  # Get user choice
        
        if option == '1':
            print("Admin User selected.")
            # Add admin functionalities here
        elif option == '2':
            print("Member Customer selected.")
            # Add member customer functionalities here
        elif option == '3':
            print("Non-Member Customer selected.")
            # Add non-member customer functionalities here
        elif option == '4':
            print("Exiting...")
            break  # Exit the loop and end the program
        else:
            print("Invalid option, please try again.")

# Run the main menu
main_menu()
