from database import mycursor, mydb
from rental_management import book_car, calculate_rental_fee
import hashlib


def modify_personal_details():
    print("\n** Modify Personal Details **\n")

    username = input("Enter your current username: ")
    new_username = input("Enter new username: ")
    new_password = input("Enter new password (leave blank to keep current password): ")
    new_personal_id = input("Enter Personal ID: ")
    new_tel_no = input("Enter new telephone number: ")
    new_address = input("Enter new address: ")

    # Hash the new password if it is provided
    if new_password:
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    else:
        # If the password is not changed, retrieve the current hashed password from the database
        sql_get_password = "SELECT password FROM users WHERE username = %s"
        mycursor.execute(sql_get_password, (username,))
        hashed_password = mycursor.fetchone()[0]

    sql = """
    UPDATE users 
    SET username = %s, password = %s, personal_id = %s, tel_no = %s, address = %s
    WHERE username = %s
    """
    val = (new_username, hashed_password, new_personal_id, new_tel_no, new_address, username)
    mycursor.execute(sql, val)
    mydb.commit()

    print("Personal details updated successfully.")

def view_rental_history():
    username = input("Enter your username: ")
    sql = "SELECT * FROM rentals WHERE customer_username = %s"
    mycursor.execute(sql, (username,))
    rentals = mycursor.fetchall()
    for rental in rentals:
        print(rental)

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


def customer_menu():
    while True:
        print("\n** Customer Menu **\n")
        print("1 = Modify personal details")
        print("2 = View rental history")
        print("3 = View details of booked car")
        print("4 = Make a car booking")
        print("5 = Make payment")
        print("6 = Logout\n")

        option = input("Select an option: ")

        if option == '1':
            modify_personal_details()
        elif option == '2':
            view_rental_history()
        elif option == '3':
            view_details_of_booked_car()
        elif option == '4':
            make_car_booking()
        elif option == '5':
            make_payment()
        elif option == '6':
            break
        else:
            print("Invalid option, please try again.")

