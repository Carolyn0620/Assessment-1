from database import Database
from menus import main_menu

if __name__ == "__main__":
    db_instance = Database()
    mydb = db_instance.get_connection()
    mycursor = mydb.cursor(buffered=True)

    main_menu(mycursor, mydb)
