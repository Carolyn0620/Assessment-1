from database import mycursor, mydb


# Function to display cars
def display_cars():
    try:
        sql = "SELECT * FROM cars"
        mycursor.execute(sql)
        cars = mycursor.fetchall()

        # Check if any cars are fetched
        if not cars:
            print("No cars found in the database.")
            return
        
        print("\n** List of Cars **")
        header = "{:<3} | {:<10} | {:<10} | {:<15} | {:<10} | {:<6} | {:<10} | {:<10} | {:<5} | {:<10} | {:<13} | {:<14} | {:<14}".format(
            "ID", "Make", "Model", "Plate Number", "Color", "Seats", "Rate/Hour", "Rate/Day", "Year", "Mileage", "Available Now", "MinRentPeriod", "MaxRentPeriod"
        )
        print(header)
        print("-" * 170)
        for car in cars:
            print("{:<3} | {:<10} | {:<10} | {:<15} | {:<10} | {:<6} | {:<10} | {:<10} | {:<5} | {:<10} | {:<13} | {:<14} | {:<14}".format(
                car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], "Yes" if car[10] else "No", car[11], car[12]
            ))
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to delete car
def delete_car():
    display_cars()  # Display the list of cars before asking for the car ID
    car_id = int(input("\nEnter the car ID to delete: "))
    confirm = input("Are you sure you want to delete this car? (Y/N): ")
    if confirm.lower() == 'y':
        sql = "DELETE FROM cars WHERE id = %s"
        mycursor.execute(sql, (car_id,))
        mydb.commit()
        print("Car deleted successfully.")
    else:
        print("Car deletion cancelled.")


