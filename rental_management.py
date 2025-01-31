from datetime import datetime
import mysql
from database import mycursor, mydb

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

# Function to calculate rental fee
def calculate_rental_fee(car_id, rental_start, rental_end):
    sql = "SELECT * FROM cars WHERE id = %s"
    mycursor.execute(sql, (car_id,))
    car = mycursor.fetchone()
    
    start_date = datetime.strptime(rental_start, "%Y-%m-%d")
    end_date = datetime.strptime(rental_end, "%Y-%m-%d")
    rental_days = (end_date - start_date).days + 1  # Include the last day
    
    daily_rate = car[7]  # Assuming rate_per_day is the 8th column (index 7) of the cars table
    total_fee = rental_days * daily_rate
    
    print(f"Total rental fee for {rental_days} days is: {total_fee}")
    return total_fee

# Function to view rental history
def view_rental_history():
    username = input("Enter your username: ")
    sql = "SELECT * FROM rentals WHERE username = %s"
    mycursor.execute(sql, (username,))
    rentals = mycursor.fetchall()

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


def book_car(username, car_id, rental_start, rental_end, total_fee, booked_by, email_address, payment_status, rental_status, return_status):
    sql = """
    INSERT INTO rentals (username, car_id, rental_start, rental_end, total_fee, booked_by, email_address, payment_status, rental_status, return_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    val = (username, car_id, rental_start, rental_end, total_fee, booked_by, email_address, payment_status, rental_status, return_status)
    mycursor.execute(sql, val)
    mydb.commit()

def view_rental_requests():
    sql = """
    SELECT rentals.id, users.name, cars.make, cars.model, rentals.rental_start, rentals.rental_end, rentals.total_fee, rentals.rental_status
    FROM rentals
    JOIN users ON rentals.username = users.username
    JOIN cars ON rentals.car_id = cars.id
    WHERE rentals.rental_status = 'pending'
    """
    mycursor.execute(sql)
    requests = mycursor.fetchall()

    if requests:
        print("\n========== Pending Rental Requests ==========")
        print(f"{'Request ID':<10}{'Customer':<20}{'Car':<20}{'Rental Start':<15}{'Rental End':<15}{'Total Fee':<10}{'Payment Status':<10}{'Rental Status':<10}{'Return Status':<10}")
        print("=" * 100)
        for request in requests:
            print(f"{request[0]:<10}{request[1]:<20}{request[2] + ' ' + request[3]:<20}{str(request[4]):<15}{str(request[5]):<15}{request[6]:<10}{request[7]:<10}")
        print("=" * 100)
    else:
        print("No pending rental requests found.")

def manage_rental_requests():
    while True:
        view_rental_requests()
        request_id = input("Enter the Request ID to approve/reject (or 'Q' to quit): ")
        
        if request_id.strip().lower() == 'q':
            break

        action = input("Enter 'A' to approve or 'R' to reject the request: ").strip().lower()
        if action == 'a':
            update_status(request_id, 'approved')
        elif action == 'r':
            update_status(request_id, 'rejected')
        else:
            print("Invalid action. Please enter 'A' to approve or 'R' to reject.")

def update_status(request_id, rental_status):
    sql = "UPDATE rentals SET rental_status = %s WHERE id = %s"
    val = (rental_status, request_id)
    mycursor.execute(sql, val)
    mydb.commit()
    print(f"Request ID {request_id} has been {rental_status}.")

def display_rentals():
    sql = """
    SELECT rentals.id, rentals.username, rentals.car_id, rentals.rental_start, rentals.rental_end, rentals.total_fee, rentals.booked_by, rentals.email_address, rentals.payment_status, rentals.rental_status, rentals.return_status
    FROM rentals
    """
    mycursor.execute(sql)
    rentals = mycursor.fetchall()

    if rentals:
        print("\n========== Rentals Table ==========")
        print(f"{'Rental ID':<10}{'Username':<15}{'Car ID':<10}{'Rental Start':<15}{'Rental End':<15}{'Total Fee':<10}{'Booked By':<15}{'Email Address':<25}{'Payment Status':<15}{'Rental Status':<15}{'Return Status':<15}")
        print("=" * 180)
        for rental in rentals:
            print(f"{rental[0]:<10}{rental[1]:<15}{rental[2]:<10}{str(rental[3]):<15}{str(rental[4]):<15}{rental[5]:<10}{rental[6]:<15}{rental[7]:<25}{rental[8]:<15}{rental[9]:<15}{rental[10]:<15}")
        print("=" * 180)
    else:
        print("No rental records found.")

def update_payment(rental_id, amount, payment_method):
    try:
        # Insert payment details into the payments table
        sql_payment = "INSERT INTO payments (rental_id, amount, payment_method) VALUES (%s, %s, %s)"
        val_payment = (rental_id, amount, payment_method)
        mycursor.execute(sql_payment, val_payment)
        
        # Update the payment_status in the rentals table
        sql_update_status = "UPDATE rentals SET payment_status = 'paid' WHERE id = %s"
        mycursor.execute(sql_update_status, (rental_id,))
        
        mydb.commit()
        print("Payment recorded and status updated to 'paid' successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def return_rented_car(rental_id):
    try:
        confirm = input(f"You entered '{rental_id}'. Please make sure the information is correct. Proceed? (Y/N): ")
        if confirm.lower() == 'y':
            sql = "UPDATE rentals SET return_status = 'returned' WHERE id = %s"
            mycursor.execute(sql, (rental_id,))
            mydb.commit()
            print("Rental return status updated to 'returned' successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

