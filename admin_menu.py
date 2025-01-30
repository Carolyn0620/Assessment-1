from database import mycursor, mydb
from car_management import display_cars, delete_car
from rental_management import update_payment, return_rented_car, book_car
from utils import get_valid_input, is_positive_int, is_string, is_float

def admin_menu():
    while True:
        print("\n** Admin Menu **\n")
        print("1 = Add Car")
        print("2 = Modify Car")
        print("3 = Display Car")
        print("4 = Delete Car")
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
                available_now = get_valid_input("Is the car available now? (Y = Yes, N = No): ", lambda x: x.lower() in ['y', 'n']).lower()
                min_rent_period = int(get_valid_input("Enter minimum rent period (day): ", is_positive_int))
                max_rent_period = int(get_valid_input("Enter maximum rent period (day): ", is_positive_int))
                
                # Convert 'Y'/'N' to 1/0
                available_now = 1 if available_now == 'y' else 0

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
                print(f"Available Now: {'Yes' if available_now else 'No'}")
                print(f"Minimum Rent Period: {min_rent_period}")
                print(f"Maximum Rent Period: {max_rent_period}")

                confirm = input("Are you sure you want to save the record? (Y/N): ")
                if confirm.lower() == 'y':
                    sql = """
                    INSERT INTO cars (
                        make, model, plate_number, color, seats, rate_per_hour, 
                        rate_per_day, year, mileage, available_now,
                        min_rent_period, max_rent_period
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            # Display the list of cars before asking for the car ID
            display_cars()

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
            available_now = get_valid_input("Is the car available now? (Y = Yes, N = No): ", lambda x: x.lower() in ['y', 'n']).lower()
            min_rent_period = int(get_valid_input("Enter new minimum rent period (day): ", is_positive_int))
            max_rent_period = int(get_valid_input("Enter new maximum rent period (day): ", is_positive_int))
                
            # Convert 'Y'/'N' to 1/0
            available_now = 1 if available_now == 'y' else 0

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
            print(f"Available Now: {'Yes' if available_now else 'No'}")
            print(f"Minimum Rent Period: {min_rent_period}")
            print(f"Maximum Rent Period: {max_rent_period}")

            confirm = input("Are you sure you want to save the record? (Y/N): ")
            if confirm.lower() == 'y':
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
            
            else:
                reenter = input("Car record not saved. Re-enter the details? (Y/N): ")
                if reenter.lower() == 'y':
                    continue  # This will loop back to re-enter car details
                else:
                     break
            
        elif option == '3':
            display_cars()
        elif option == '4':
            delete_car()
            display_cars()
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
