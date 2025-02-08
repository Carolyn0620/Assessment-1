from rental_management import calculate_rental_fee
from rental_management import book_car
from tabulate import tabulate
from datetime import datetime
from db_config import connect_to_db

# Get database instance
connection = connect_to_db()
cursor = connection.cursor()

def display_cars():
    try:
        sql = "SELECT * FROM cars"
        cursor.execute(sql)
        cars = cursor.fetchall()

        # Check if any cars are fetched
        if not cars:
            print("No cars found in the database.")
            return
        
        print("\n** List of Cars **")
        headers = ["ID", "Make", "Model", "Plate Number", "Color", "Seats", "Rate/Hour", "Rate/Day", "Year", "Mileage", "Available Now", "MinRentPeriod", "MaxRentPeriod"]
        table = []
        for car in cars:
            table.append([
                car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], "Yes" if car[10] else "No", car[11], car[12]
            ])
        print(tabulate(table, headers, tablefmt="grid"))
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to delete car
def delete_car(car_id):
    try:
        # Delete the car from the database
        sql_delete = "DELETE FROM cars WHERE id = %s"
        cursor.execute(sql_delete, (car_id,))
        connection.commit()
        print(f"Car with ID {car_id} deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_details_of_booked_car():
    while True:
        username = input("Enter your username: ")
        if username.strip():
            break
        print("Invalid input. Please enter a valid username.")

    sql = """
    SELECT cars.*
    FROM rentals
    JOIN cars ON rentals.car_id = cars.id
    WHERE rentals.username = %s AND rentals.rental_end >= CURDATE()
    """
    cursor.execute(sql, (username,))
    cars = cursor.fetchall()

    if cars:
        print("\n========== Details of Booked Cars ==========")
        print(f"{'CarID':<10}{'Make':<15}{'Model':<15}{'PlateNumber':<15}{'Color':<10}{'Seats':<6}{'RatePerHour':<15}{'RatePerDay':<15}{'Year':<6}{'Mileage':<8}{'AvailableNow':<15}{'MinRentPeriod':<15}{'MaxRentPeriod':<15}")
        print("=" * 150)
        for car in cars:
            print(f"{car[0]:<10}{car[1]:<15}{car[2]:<15}{car[3]:<15}{car[4]:<10}{car[5]:<6}{car[6]:<15}{car[7]:<15}{car[8]:<6}{car[9]:<8}{'Yes' if car[10] else 'No':<15}{car[11]:<15}{car[12]:<15}")
    else:
        print("No booked cars found for the given username.")

    while True:
        confirm = input("Would you like to continue booking a car? (Y/N): ")
        if confirm.lower() == 'n':
            break
        elif confirm.lower() == 'y':
            make_car_booking()


# Function to make car booking
def make_car_booking():
    # Validate username
    while True:
        username = input("Enter your username: ")
        if username.strip():  # Check if the input is not empty
            confirm = input("Please make sure the information is correct. Proceed? (Y/N): ")
            if confirm.lower() == 'y':
                break
        print("Invalid input. Please enter a valid username.")
    
    # Validate car ID
    while True:
        try:
            car_id = int(input("Enter car ID to book: "))
            confirm = input("Please make sure the information is correct. Proceed? (Y/N): ")
            if confirm.lower() == 'y':
                break
        except ValueError:
            print("Invalid input. Car ID must be a number. Please try again.")

    # Validate rental start date
    while True:
        rental_start = input("Enter rental start date (YYYY-MM-DD): ")
        try:
            datetime.strptime(rental_start, "%Y-%m-%d")
            confirm = input("Please make sure the information is correct. Proceed? (Y/N): ")
            if confirm.lower() == 'y':
                break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    # Validate rental end date
    while True:
        rental_end = input("Enter rental end date (YYYY-MM-DD): ")
        try:
            datetime.strptime(rental_end, "%Y-%m-%d")
            confirm = input("Please make sure the information is correct. Proceed? (Y/N): ")
            if confirm.lower() == 'y':
                break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    # Validate booked by
    while True:
        booked_by = input("Enter the name of the person booking the car: ")
        if booked_by.strip():  # Check if the input is not empty
            confirm = input("Please make sure the information is correct. Proceed? (Y/N): ")
            if confirm.lower() == 'y':
                break
        print("Invalid input. Please enter a valid name.")

    # Validate email address
    while True:
        email_address = input("Enter email address: ")
        if email_address.strip():  # Check if the input is not empty
            confirm = input("Please make sure the information is correct. Proceed? (Y/N): ")
            if confirm.lower() == 'y':
                break
        print("Invalid input. Please enter a valid email address.")

    total_fee = calculate_rental_fee(car_id, rental_start, rental_end)
    book_car(username, car_id, rental_start, rental_end, total_fee, booked_by, email_address)


