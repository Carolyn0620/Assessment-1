import hashlib
from database import mycursor, mydb

def register_user(username, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    val = (username, hashed_password, role)
    mycursor.execute(sql, val)
    mydb.commit()
    print("User registered successfully.")

def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username, hashed_password)
    mycursor.execute(sql, val)
    return mycursor.fetchone()

def log_query(sql, val=None):
    log_sql = "INSERT INTO query_log (query, query_values) VALUES (%s, %s)"
    log_val = (sql, str(val) if val else 'NULL')
    mycursor.execute(log_sql, log_val)
    mydb.commit()
