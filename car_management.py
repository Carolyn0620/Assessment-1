from database import mycursor, mydb
from rental_management import calculate_rental_fee
from rental_management import book_car

# Function to display cars
def display_cars():
    try:
        sql = "SELECT * FROM cars"
        mycursor.execute(sql)
        cars = mycursor.fetchall()

        # Check if any cars are fetched
        if not cars:
            print("No cars found in the database.")
            return
        
        print("\n** List of Cars **")
        header = "{:<3} | {:<10} | {:<10} | {:<15} | {:<10} | {:<6} | {:<10} | {:<10} | {:<5} | {:<10} | {:<13} | {:<14} | {:<14}".format(
            "ID", "Make", "Model", "Plate Number", "Color", "Seats", "Rate/Hour", "Rate/Day", "Year", "Mileage", "Available Now", "MinRentPeriod", "MaxRentPeriod"
        )
        print(header)
        print("-" * 170)
        for car in cars:
            print("{:<3} | {:<10} | {:<10} | {:<15} | {:<10} | {:<6} | {:<10} | {:<10} | {:<5} | {:<10} | {:<13} | {:<14} | {:<14}".format(
                car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], "Yes" if car[10] else "No", car[11], car[12]
            ))
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to delete car
def delete_car(car_id):
    # Delete the car from the database
    sql_delete = "DELETE FROM cars WHERE id = %s"
    mycursor.execute(sql_delete, (car_id,))
    mydb.commit()
    print(f"Car with ID {car_id} deleted successfully.")

# Function to view detals of booked car
def view_details_of_booked_car():
    username = input("Enter your username: ")
    sql = """
    SELECT cars.*
    FROM rentals
    JOIN cars ON rentals.car_id = cars.id
    WHERE rentals.customer_username = %s AND rentals.rental_end >= CURDATE()
    """
    mycursor.execute(sql, (username,))
    cars = mycursor.fetchall()
    for car in cars:
        print(car)

# Function to make car booking
def make_car_booking():
    username = input("Enter your username: ")
    car_id = int(input("Enter car ID to book: "))
    rental_start = input("Enter rental start date (YYYY-MM-DD): ")
    rental_end = input("Enter rental end date (YYYY-MM-DD): ")
    total_fee = calculate_rental_fee(car_id, rental_start, rental_end)
    book_car(username, car_id, rental_start, rental_end, total_fee)

def make_payment():
    username = input("Enter your username: ")
    # Implement make payment functionality
    pass
