import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Carolyn123",
    database="python_crs"
)

mycursor = mydb.cursor()

def create_database_schema():
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
        user_id INT NOT NULL,
        car_id INT NOT NULL,
        rental_start DATE NOT NULL,
        rental_end DATE NOT NULL,
        total_fee FLOAT NOT NULL,
        status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (car_id) REFERENCES cars(id)
    )
    """)
    
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rental_id INT NOT NULL,
        amount FLOAT NOT NULL,
        payment_method ENUM('Cash', 'Cheque') NOT NULL,
        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (rental_id) REFERENCES rentals(id)
    )
    """)
    
    mydb.commit()
