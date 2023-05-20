import mysql.connector
import database

def registerMember():
    # Get user input
    firstName = input("First name: ")
    lastName = input("Last name: ")
    address = input("Street address: ")
    city = input("City: ")
    state = input("State: ")
    while True:
        try:
            zip = int(input("Zip code: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    phone = input("Phone: ")
    email = input("Email: ")
    while True:
        try:
            userId = int(input("Enter your user ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")    
    password = input("Password: ")
    creditCardType = input("Creditcardtype: ")
    creditCardNumber = input("Creditcardnumber: ")

    # Insert the member into the database
    try:
        connection = database.getDatabaseConnection()
        cursor = connection.cursor()

        query = "INSERT INTO members (userid, fname, lname, address, city, state, zip, phone, email, password, creditcardtype, creditcardnumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (userId, firstName, lastName, address, city, state, zip, phone, email, password, creditCardType, creditCardNumber)

        cursor.execute(query, values)
        connection.commit()

        print("Member registered successfully.")

    except mysql.connector.Error:
        print("Error: Could not register member. Please revise your input.")

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()