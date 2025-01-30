from database import create_database_schema
from database import mycursor, mydb
from admin_menu import admin_menu
from customer_menu import customer_menu, modify_personal_details
from utils import get_valid_input, is_positive_int, is_string
import hashlib

def main_menu():
    create_database_schema()

    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit\n")
        option = input("Select an option: ")
        
        if option == '1':
            login()
        elif option == '2':
            register()
        elif option == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

# Default admin credentials
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "adminpass" 

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password(hashed_password, user_password):
    return hashed_password == hashlib.sha256(user_password.encode('utf-8'))

def login():
    username = input("\nEnter username: ")
    password = input("Enter password: ")
    
    if username == DEFAULT_ADMIN_USERNAME and password == DEFAULT_ADMIN_PASSWORD: 
        print("\n** Default Admin Login Successful. **\n")
        print("1. Update Admin Details")
        print("2. New Admin\n")
        admin_choice = input("Select an option: ")

        if admin_choice == '1':
            modify_personal_details()
        elif admin_choice == '2':
            register_admin()
        else:
            print("Invalid option, returning to main menu.")
    else:
        hashed_password = hash_password(password)
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        val = (username, hashed_password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        
        if user:
            if user[3] == 'admin':  # Role is in the 4th column (index 3) in the users table.
                print(f"Admin login successful.")
                admin_menu()
            elif user[3] == 'customer':
                print(f"Customer login successful.")
                customer_menu()
        else:
            print("Invalid username or password. Please try again.")

def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    hashed_password = hash_password(password)
    
    sql = "SELECT * FROM users WHERE username = %s AND password = %s AND role = 'admin'"
    val = (username, hashed_password)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    
    if user:
        print(f"Admin login successful. Welcome, {user[1]}!")
        admin_menu()
    else:
        print("Invalid admin credentials. Please try again.")

def register():
    register_customer()

def register_admin():
    print("\n** Register New Admin **\n")
    name = get_valid_input("Enter name: ", is_string)
    personal_id = get_valid_input("Enter Personal ID: ", is_positive_int)
    tel_no = get_valid_input("Enter Tel. No: ", is_string)
    address = get_valid_input("Enter address: ", is_string)
    username = get_valid_input("Enter username: ", is_string)
    password = get_valid_input("Enter password: ", is_string)
    hashed_password = hash_password(password)
    
    sql = "INSERT INTO users (name, personal_id, tel_no, address, username, password, role) VALUES (%s, %s, %s, %s, %s, %s, 'admin')"
    val = (name, personal_id, tel_no, address, username, hashed_password)
    mycursor.execute(sql, val)
    mydb.commit()
    print("New admin registered successfully.")

def register_customer():
    print("\n** Register New Customer **\n")
    name = get_valid_input("Enter name: ", is_string)
    personal_id = get_valid_input("Enter Personal ID: ", is_positive_int)
    tel_no = get_valid_input("Enter Tel. No: ", is_string)
    address = get_valid_input("Enter address: ", is_string)
    username = get_valid_input("Enter username: ", is_string)
    password = get_valid_input("Enter password: ", is_string)
    hashed_password = hash_password(password)
    
    sql = "INSERT INTO users (name, personal_id, tel_no, address, username, password, role) VALUES (%s, %s, %s, %s, %s, %s, 'customer')"
    val = (name, personal_id, tel_no, address, username, hashed_password)
    mycursor.execute(sql, val)
    mydb.commit()
    print("New customer registered successfully.")

main_menu()
