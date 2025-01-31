from database import mycursor, mydb
from user_management import modify_personal_details
from rental_management import view_rental_history
from car_management import view_details_of_booked_car, make_car_booking, display_cars
from utils import get_valid_input, validate_current_username, validate_new_username, validate_password, validate_tel_no, validate_address, is_string


def customer_menu():
    while True:
        print("\n** Customer Menu **\n")
        print("1 = Modify personal details")
        print("2 = View rental history")
        print("3 = View details of booked car")
        print("4 = Make a car booking")
        print("5 = Logout\n")

        option = input("Select an option: ")

        if option == '1':
            while True:
                print("\n** Modify Personal Details **\n")
                modify_personal_details()

        elif option == '2':
            # View rental history
            view_rental_history()

        elif option == '3':
            view_details_of_booked_car()

        elif option == '4':
            while True:
                display_cars()
                make_car_booking()
                confirm = input("Would you like to make another booking? (Y/N): ")
                if confirm.lower() == 'y':
                    continue  # This will loop back to make another booking
                else:
                    break

        elif option == '5':
            print("Logging out. Goodbye!")
            break  # Exit the loop and log out

        else:
            print("Invalid option, please try again.")

