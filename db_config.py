import sqlite3


def connect_to_db():
    # Establishes and returns a connection to the SQLite database.
    return sqlite3.connect("car_rental.db")


def safe_query(query, params=()):
    try:
        conn = sqlite3.connect("car_rental.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

