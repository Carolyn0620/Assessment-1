from user_management import User
from rental_management import view_rental_history
from car_management import view_details_of_booked_car, make_car_booking, display_cars

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
            User.modify_personal_details()

        elif option == '2':
            view_rental_history()

        elif option == '3':
            view_details_of_booked_car()

        elif option == '4':
            while True:
                display_cars()
                make_car_booking()
                confirm = input("Would you like to make another booking? (Y/N): ")
                if confirm.lower() == 'y':
                    continue
                else:
                    break

        elif option == '5':
            print("Logging out. Goodbye!")
            break

        else:
            print("Invalid option, please try again.")

