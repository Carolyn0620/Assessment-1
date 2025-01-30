from datetime import datetime
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
    
    daily_rate = car[7]  # Assuming rate_per_day is the 8th column (index 7) of the cars table
    total_fee = rental_days * daily_rate
    
    print(f"Total rental fee for {rental_days} days is: {total_fee}")
    return total_fee
