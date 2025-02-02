import mysql.connector

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = cls._connect()
        return cls._instance

    @staticmethod
    def _connect():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Carolyn123",
            database="python_crs"
        )

    def get_connection(self):
        return self._instance.connection

    def get_cursor(self):
        return self._instance.connection.cursor()

# Function to create tables
def create_database_schema():
    db = Database().get_connection()
    mycursor = db.cursor()
    
    mycursor.execute("CREATE DATABASE IF NOT EXISTS python_crs")
    mycursor.execute("USE python_crs")
    
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        personal_id VARCHAR(255) NOT NULL,
        tel_no VARCHAR(255) NOT NULL,
        address TEXT NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL
    )
    """)

    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INT AUTO_INCREMENT PRIMARY KEY,
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
    )
    """)

    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        car_id INT NOT NULL,
        rental_start DATE NOT NULL,
        rental_end DATE NOT NULL,
        total_fee FLOAT NOT NULL,
        booked_by VARCHAR(255) NOT NULL,
        email_address VARCHAR(255) NOT NULL,
        payment_status ENUM('paid', 'unpaid') DEFAULT 'unpaid',
        rental_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
        return_status ENUM('returned', 'pending') DEFAULT 'pending',
        FOREIGN KEY (username) REFERENCES users(username),
        FOREIGN KEY (car_id) REFERENCES cars(id)
    )
    """)

    db.commit()
