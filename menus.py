from user_menu import User, Customer
from database import create_database_schema

def main_menu(mycursor, mydb):
    create_database_schema()

    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit\n")
        option = input("Select an option: ")

        if option == '1':
            username = input("\nEnter username: ")
            password = input("Enter password: ")
            User.login(username, password, mycursor, mydb)

        elif option == '2':
            Customer.register_customer(mycursor, mydb)
        elif option == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")
