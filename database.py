import mysql.connector

def getDatabaseConnection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="example",
            database="book_store"
        )
    except mysql.connector.Error as error:
        print(f"Error: {error}")