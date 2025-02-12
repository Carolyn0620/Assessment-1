from rental_management import calculate_rental_fee, book_car
from database import Database
from tabulate import tabulate
from utils import Validator



def add_car_to_db(make, model, plate_number, color, seats, rate_per_hour, rate_per_day, year, mileage, available_now, min_rent_period, max_rent_period):
    # Add a new car to the database.
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()

    try:
        sql = ("INSERT INTO cars (make, model, plate_number, color, seats, rate_per_hour, rate_per_day, year, mileage, available_now, min_rent_period, max_rent_period) "
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        values = (make, model, plate_number, color, seats, rate_per_hour, rate_per_day, year, mileage, available_now, min_rent_period, max_rent_period)

        cursor.execute(sql, values)
        connection.commit()
        print("Car added successfully!")

    except Exception as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        connection.close()

def view_available_cars():
    
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()

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
                car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], car[10], car[11], car[12]
            ])
        print(tabulate(table, headers, tablefmt="grid"))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

# Function to delete car
def delete_car_from_db(car_id):

    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()

    # Delete the car from the database
    sql_delete = "DELETE FROM cars WHERE id = ?"
    cursor.execute(sql_delete, (car_id,))
    connection.commit()
    print(f"Car with ID {car_id} deleted successfully.")

def update_car_to_db(car_id, mileage, available_now):
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()
        
    sql = """
    UPDATE cars SET mileage=?, available_now=? WHERE id=?
    """
    val = (mileage, available_now, car_id)
    cursor.execute(sql, val)
    connection.commit()
    print("Car details updated successfully.")

    cursor.close()
    connection.close()
    view_available_cars()

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



