import sqlite3

class Database:
    def __init__(self, db_name='crs_data.db'):
        """Initialize with the database name."""
        self.db_name = db_name

    def connect_to_db(self):
        """Connect to the SQLite database and return the connection."""
        return sqlite3.connect(self.db_name)

    def execute_query(self, query, params=()):
        """
        Execute a query (e.g., INSERT, UPDATE, DELETE).
        Commits the changes to the database.
        """
        connection = self.connect_to_db()
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()

    def fetch_one(self, query, params=()):
        """Fetch one result (e.g., for SELECT queries)."""
        connection = self.connect_to_db()
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()
        return result

    def fetch_all(self, query, params=()):
        """Fetch all results (e.g., for SELECT queries)."""
        connection = self.connect_to_db()
        cursor = connection.cursor()
        results = []
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()
        return results
