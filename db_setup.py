import sqlite3


def create_tables():
    # Connect to SQLite database (creates `crs_data.db` if it doesn't exist)
    connection = sqlite3.connect("crs_data.db")
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
            available_now VARCHAR(255) NOT NULL,
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
            payment_status VARCHAR(255) NOT NULL,
            rental_status VARCHAR(255) NOT NULL,
            return_status VARCHAR(255) NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (car_id) REFERENCES cars(id)
    );
    ''')

    # Call these methods to create sample databases of users, cars and bookings for testing purpose
    # initial_user_DB(cursor)
    # initial_car_db(cursor)
    # initial_booking_db(cursor)

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
        ('Toyota', 'Camry', 'ABC123', 'Red', 5, 10.0, 60.0, 2020, 15000, 1, 1, 30),
        ('Honda', 'Civic', 'DEF456', 'Blue', 5, 9.0, 55.0, 2019, 20000, 1, 1, 30),
        ('Ford', 'Mustang', 'GHI789', 'Black', 4, 15.0, 90.0, 2021, 5000, 1, 1, 30)
    ]

    for car in cars:
        cursor.execute('''INSERT INTO cars (make, model, plate_number, color, seats, rate_per_hour, rate_per_day, year, mileage, available_now, min_rent_period, max_rent_period)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', car)


def initial_rental_db(cursor):
    # Insert data into rentals table (Initial data for testing purposes)
    rentals = [
        ('john_doe', 1, '2023-06-01', '2023-06-05', 300.0, 'John Doe', 'john@example.com', 'confirmed', 'returned'),
        ('jane_smith', 2, '2023-07-10', '2023-07-15', 275.0, 'Jane Smith', 'jane@example.com', 'confirmed', 'pending'),
        ('bob_jones', 3, '2023-08-20', '2023-08-25', 450.0, 'Bob Jones', 'bob@example.com', 'confirmed', 'returned')
    ]

    for rental in rentals:
        cursor.execute('''INSERT INTO bookings (user_id, car_id, start_date, end_date, total_cost, status) 
                                    VALUES (?, ?, ?, ?, ?, ?)''', rental)


# Run the script to create tables
if __name__ == "__main__":
    create_tables()
