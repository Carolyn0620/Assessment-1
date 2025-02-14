from database import Database
from datetime import datetime
import sqlite3
from tabulate import tabulate

db = Database()
connection = db.connect_to_db()
cursor = connection.cursor()

def view_rentals_requests():
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()
    
    sql = """
    SELECT rentals.id, users.name, cars.make, cars.model, rentals.rental_start, rentals.rental_end, rentals.total_fee, rentals.rental_status
    FROM rentals
    JOIN users ON rentals.username = users.username
    JOIN cars ON rentals.car_id = cars.id
    WHERE rentals.rental_status = 'pending'
    """
    cursor.execute(sql)
    requests = cursor.fetchall()

    if requests:
        print("\n========== Pending Rental Requests ==========")
        print(f"{'Request ID':<10}{'Customer':<20}{'Car':<20}{'Rental Start':<15}{'Rental End':<15}{'Total Fee':<10}{'Rental Status':<15}")
        print("=" * 100)
        for request in requests:
            print(f"{request[0]:<10}{request[1]:<20}{request[2] + ' ' + request[3]:<20}{str(request[4]):<15}{str(request[5]):<15}{request[6]:<10}{request[7]:<15}")
        print("=" * 100)
    else:
        print("No pending rental requests found.")
    
    cursor.close()
    connection.close()

def update_rental_status(request_id, rental_status):
    sql = "UPDATE rentals SET rental_status = ? WHERE id = ?"
    val = (rental_status, request_id)
    cursor.execute(sql, val)
    connection.commit()
    print(f"Request ID {request_id} has been {rental_status}.")
    display_rentals_table()
    
# Function to update customer payment
def update_payment_status_to_db(id, payment_status):
    
    if payment_status not in ['paid', 'unpaid']:
        print("Error: Invalid payment status. Must be 'paid' or 'unpaid'.")
        return
    
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()
        
    sql = """
    UPDATE rentals SET payment_status=? WHERE id=?
    """
    val = (payment_status, id)
    cursor.execute(sql, val)
    connection.commit()
    print("Payment status updated successfully.")

    cursor.close()
    connection.close()
    display_rentals_table()


# Function to return a rented car
def update_returned_car_to_db(car_id, return_status):
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()
        
    try:
        # Update return_status in the rentals table
        sql_update_status = "UPDATE rentals SET return_status = ? WHERE car_id = ?"
        cursor.execute(sql_update_status, (return_status, car_id))
        connection.commit()
        print("Return status updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()
        display_rentals_table()

# Function to view rental history
def view_rental_history():
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
        print(f"Rental Status: {rental[9]}")
        print(f"Return Status: {rental[10]}")

# Function to calculate rental fee
def calculate_rental_fee(car_id, rental_start, rental_end):
    sql = "SELECT rate_per_day FROM cars WHERE id = ?"
    cursor.execute(sql, (car_id,))
    car = cursor.fetchone()
    
    start_date = datetime.strptime(rental_start, "%Y-%m-%d")
    end_date = datetime.strptime(rental_end, "%Y-%m-%d")
    rental_days = (end_date - start_date).days + 1  # Include the last day
    
    daily_rate = car[0]  # Assuming rate_per_day is the first column
    total_fee = rental_days * daily_rate
    
    total_fee = round(total_fee, 2)

    print(f"Total rental fee for {rental_days} days is: {total_fee:.2f}")
    return total_fee

def book_car(username, car_id, rental_start, rental_end, total_fee, booked_by, email_address, rental_status="pending", return_status="pending", payment_status="unpaid"):
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()

    try:
        sql = '''
        INSERT INTO rentals (username, car_id, rental_start, rental_end, total_fee, booked_by, email_address, rental_status, return_status, payment_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        values = (username, car_id, rental_start, rental_end, total_fee, booked_by, email_address, rental_status, return_status, payment_status)
        cursor.execute(sql, values)
        connection.commit()
        print("Car booking successful!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        





def manage_rental_requests():
    while True:
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
    sql = "UPDATE rentals SET rental_status = ? WHERE id = ?"
    val = (rental_status, request_id)
    cursor.execute(sql, val)
    connection.commit()
    print(f"Request ID {request_id} has been {rental_status}.")

def display_rentals_table():
    db = Database()
    connection = db.connect_to_db()
    cursor = connection.cursor()

    try:
        sql = "SELECT * FROM rentals"
        cursor.execute(sql)
        rentals = cursor.fetchall()
        
        # Check if any rentals are fetched
        if not rentals:
            print("No rentals found in the database.")
            return
  
        print("\n** Rentals Table **")
        headers = ["Rental ID", "Username", "Car ID", "Rental Start", "Rental End", "Total Fee", "Booked By", "Email Address", "Rental Status", "Return Status",  "Payment Status"]
        table = []
        for rental in rentals:
            table.append([
                rental[0], rental[1], rental[2], str(rental[3]), str(rental[4]), rental[5], rental[6], rental[7], rental[8], rental[9], rental[10]
            ])
            print(tabulate(table, headers, tablefmt="fancy_grid"))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()



def return_rented_car(rental_id):
    try:
        confirm = input(f"You entered '{rental_id}'. Please make sure the information is correct. Proceed? (Y/N): ")
        if confirm.lower() == 'y':
            sql = "UPDATE rentals SET return_status = 'returned' WHERE id = ?"
            cursor.execute(sql, (rental_id,))
            connection.commit()
            print("Rental return status updated to 'returned' successfully.")
    except sql.connector.Error as err:
        print(f"Error: {err}")



