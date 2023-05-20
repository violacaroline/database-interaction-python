import mysql.connector
import database

def loginMember():
    # Get user input
    userid = input("User ID: ")
    password = input("Password: ")


    # Check if the userid and password match a member in the database
    try:
        connection = connection = database.getDatabaseConnection()
        cursor = connection.cursor()

        query = "SELECT * FROM members WHERE userid = %s"
        values = (userid,)

        cursor.execute(query, values)

        member = cursor.fetchone()
        if member is None:
            print("Invalid userid or password")
            return

        # Compare the password entered during login with the stored password
        if password == member[2]:
            print("Login successful.")
            return True
        else:
            print("Invalid userid or password.")
            return False

    except mysql.connector.Error as error:
        print("Failed to fetch member from MySQL table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()