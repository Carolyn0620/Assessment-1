from car_management import display_cars, delete_car
from rental_management import update_payment, return_rented_car, manage_rental_requests, display_rentals
from utils import Validator
from db_config import connect_to_db

# Initialize database connection and cursor
connection = connect_to_db()
cursor = connection.cursor()

class Admin():
    def __init__(self, username, password, mycursor, mydb):
        super().__init__(username, password, "admin", mycursor, mydb)
        self.mydb = mydb
        self.mycursor = mycursor

    def admin_menu(self):
        while True:
            print("\n** Default Admin Menu **\n")
            print("1. Modify Admin Details")
            print("2. Register New Admin")
            print("3. Main Menu")
            option = input("Select an option: ")

            if option == '1':
                self.modify_admin_details()
            elif option == '2':
                self.register_new_admin()
            elif option == '3':
                break  # Return to the previous menu
            else:
                print("Invalid option, please try again.")

class AdminMenu:
    def __init__(self):
        self.run()
    
    def run(self):
        while True:
            print("\n** Admin Menu **\n")
            print("1 = Add Car")
            print("2 = Modify Car")
            print("3 = Display Car")
            print("4 = Delete Car")
            print("5 = Update Customer Payment (Cash/Credit Card)")
            print("6 = Return Rented Car")
            print("7 = Manage Rental Requests")
            print("8 = Return to Previous Menu\n")
            
            option = input("Select an option: ")
            
            if option == '1':
                self.add_car()
            elif option == '2':
                self.modify_car()
            elif option == '3':
                display_cars()
            elif option == '4':
                self.delete_car()
            elif option == '5':
                self.update_customer_payment()
            elif option == '6':
                self.return_rented_car()
            elif option == '7':
                manage_rental_requests()
            elif option == '8':
                break  # Exit the loop
            else:
                print("Invalid option, please try again.")
    
    def add_car(self):
        while True:
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
            available_now = 1 if available_now == 'y' else 0
            
            sql = """
            INSERT INTO cars (make, model, plate_number, color, seats, rate_per_hour, rate_per_day, year, mileage, available_now, min_rent_period, max_rent_period)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (make, model, plate_number, color, seats, rate_per_hour, rate_per_day, year, mileage, available_now, min_rent_period, max_rent_period)
            cursor.execute(sql, val)
            connection.commit()
            print("Car added successfully.")
            break
    
    def modify_car(self):
        display_cars()
        car_id = int(input("\nEnter the car ID to modify: "))
        make = Validator.get_valid_input("Enter new car make: ", Validator.is_string)
        make = Validator.get_valid_input("Enter new car make: ", Validator.is_string)
        model = Validator.get_valid_input("Enter new car model: ", Validator.is_string)
        plate_number = input("Enter new car plate number: ")
        color = Validator.get_valid_input("Enter new car colour: ", Validator.is_string)
        seats = int(Validator.get_valid_input("Enter new number of seats: ", Validator.is_positive_int))
        rate_per_hour = float(Validator.get_valid_input("Enter new rate per hour: ", Validator.is_float))
        rate_per_day = float(Validator.get_valid_input("Enter new rate per day: ", Validator.is_float))
        year = int(Validator.get_valid_input("Enter new car year: ", Validator.is_positive_int))
        mileage = int(Validator.get_valid_input("Enter new car mileage: ", Validator.is_positive_int))
        available_now = Validator.get_valid_input("Is the car available now? (Y = Yes, N = No): ", lambda x: x.lower() in ['y', 'n']).lower()
        min_rent_period = int(Validator.get_valid_input("Enter new minimum rent period (day): ", Validator.is_positive_int))
        max_rent_period = int(Validator.get_valid_input("Enter new maximum rent period (day): ", Validator.is_positive_int))
        available_now = 1 if available_now == 'y' else 0
        
        sql = """
        UPDATE cars SET make=%s, model=%s, plate_number=%s, color=%s, seats=%s, rate_per_hour=%s, 
        rate_per_day=%s, year=%s, mileage=%s, available_now=%s, min_rent_period=%s, 
        max_rent_period=%s WHERE id=%s
        """
        val = (make, model, plate_number, color, seats, rate_per_hour, rate_per_day, year, mileage, available_now, min_rent_period, max_rent_period, car_id)
        cursor.execute(sql, val)
        connection.commit()
        print("Car details updated successfully.")
    
    def delete_car(self):
        display_cars()
        try:
            car_id = int(input("Enter the car ID to delete: "))
            delete_car(car_id)
        except ValueError:
            print("Invalid ID. Please enter a numeric value.")
    
    def update_customer_payment(self):
        display_rentals()
        rental_id = int(input("Enter rental ID: "))
        amount = float(input("Enter payment amount: "))
        payment_method = input("Enter payment method (Cash/Credit Card): ")
        update_payment(rental_id, amount, payment_method)
    
    def return_rented_car(self):
        display_rentals()
        try:
            rental_id = int(input("Enter rental ID to return car: "))
            return_rented_car(rental_id)
        except ValueError:
            print("Invalid input. Rental ID must be a number. Please try again.")
