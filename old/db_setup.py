import sqlite3
import os

def create_tables():
    # Connect to SQLite database (creates `car_rental.db` if it doesn't exist)
    db_path = "your_database.db"
    
    # Ensure the correct database file is being used
    if os.path.exists(db_path):
        print(f"Database file '{db_path}' exists.")
    else:
        print(f"Database file '{db_path}' does not exist. It will be created.")
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create a table for storing user's details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            personal_id VARCHAR(255) NOT NULL,
            tel_no VARCHAR(255) NOT NULL,
            address TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(255) NOT NULL
        );
    ''')

    # Create a table for storing car details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make VARCHAR(255) NOT NULL,
            model VARCHAR(255) NOT NULL,
            plate_number VARCHAR(255) NOT NULL,
            color VARCHAR(255) NOT NULL,
            seats INT NOT NULL,
            rate_per_hour FLOAT NOT NULL,
            rate_per_day FLOAT NOT NULL,
            year INT NOT NULL,
            mileage INT NOT NULL,
            available_now TINYINT(1) NOT NULL,
            min_rent_period INT NOT NULL,
            max_rent_period INT NOT NULL
        );
    ''')

    # Create a table for storing rentals details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255) NOT NULL,
            car_id INT NOT NULL,
            rental_start DATE NOT NULL,
            rental_end DATE NOT NULL,
            total_fee FLOAT NOT NULL,
            booked_by VARCHAR(255) NOT NULL,
            email_address VARCHAR(255) NOT NULL,
            rental_status VARCHAR(255) NOT NULL,
            return_status VARCHAR(255) NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (car_id) REFERENCES cars(id)
    );
    ''')


    # Call these methods to create sample databases of users, cars and bookings for testing purpose
    # initial_user_db(cursor)
    # initial_car_db(cursor)
    # initial_rental_db(cursor)

    # Commit and close connection
    connection.commit()
    connection.close()

    print("Database setup complete!")


def insert_initial_users(cursor):
    """Insert initial data into the users table."""
    users = [
        ('Srijan', 'S111', '123-456-7890', '123 Main St', 'srijan', 'sss111', 'admin'),
        ('Kwang', 'K222', '234-567-8901', '456 Park Ave', 'kwang', 'kkk111', 'admin'),
        ('Katherina', 'K333', '345-678-9012', '789 Broadway', 'katherina', 'kkk111', 'customer'),
        ('Micheal', 'M444', '456-789-0123', '101 Oak St', 'micheal', 'mmm111', 'customer'),
        ('Jesslyn', 'J555', '567-890-1234', '202 Pine St', 'jesslyn', 'jjj111', 'admin'),
        ('Jason', 'J666', '678-901-2345', '303 Cedar St', 'jason', 'jjj111', 'customer')
    ]

    for user in users:
        cursor.execute('''INSERT INTO users (name, personal_id, tel_no, address, username, password, role)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''', user)
    print("Initial user data inserted successfully")

def initial_car_db(cursor):
    # Insert data into cars table (Initial data for testing purposes)
    cars = [
        ('Proton', 'Saga', 2019, 49000, True, 1, 7),
        ('Proton', 'Wira', 2020, 90000, True, 1, 7),
        ('Proton', 'Mewa', 2018, 5000, True, 1, 7),
        ('Perodua', 'Alza', 2022, 65000, True, 1, 7),
        ('Perodua', 'Myvi', 2023, 32000, True, 1, 7),
        ('Perodua', 'Myci', 2024, 4000, True, 1, 7)
    ]

    for car in cars:
        cursor.execute('''INSERT INTO cars (make, model, year, mileage, available, min_rent_period, max_rent_period)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)''', car)


def initial_rental_db(cursor):
    # Insert data into bookings table (Initial data for testing purposes)
    bookings = [
        (9, 15, '2025-02-01', '2025-02-05', 200, 'pending'),
        (10, 23, '2025-01-31', '2025-02-04', 200, 'pending'),
        (11, 24, '2025-02-05', '2025-02-07', 100, 'pending'),
    ]

    for booking in bookings:
        cursor.execute('''INSERT INTO bookings (user_id, car_id, start_date, end_date, total_cost, status) 
                                    VALUES (?, ?, ?, ?, ?, ?)''', booking)


# Run the script to create tables
if __name__ == "__main__":
    db_path = "car_rental.db"

 # Ensure the database exists and tables are created
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' does not exist. It will be created.")
        create_tables()
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # Insert initial data
    insert_initial_users(cursor)
    initial_car_db(cursor)
    initial_rental_db(cursor)
    
    # Commit and close the connection
    connection.commit()
    connection.close()

    print("Database setup complete with sample data!")