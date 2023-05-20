import datetime
from enum import Enum
import database

class MainMenuOption(Enum):
    LOGIN = 1
    REGISTER = 2
    QUIT = 3

class MemberMenuOption(Enum):
    BROWSESUBJECT = 1
    BROWSEAUHTORANDTITLE = 2
    CHECKOUT = 3
    LOGOUT = 4

def printMainMenu():
    print("----------- MAIN MENU ------------")
    print("1. Login")
    print("2. Register New Member")
    print("3. Quit")

    # Get user menu option
    while True:
        try:
            option = int(input("Select an option: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


    if option == MainMenuOption.LOGIN.value:
        return MainMenuOption.LOGIN
    elif option == MainMenuOption.REGISTER.value:
        return MainMenuOption.REGISTER
    elif option == MainMenuOption.QUIT.value:
        print("Goodbye!")
        exit()
    else:
        print("Invalid option")

def printMemberMenu():
    print("----------- MEMBER MENU ------------")
    print("1. Browse by Subject")
    print("2. Browse by Author/Title")
    print("3. Check Out")
    print("4. Log Out")

    # Get user menu option
    while True:
        try:
            option = int(input("Select an option: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    if option == MemberMenuOption.BROWSESUBJECT.value:
        return MemberMenuOption.BROWSESUBJECT
    elif option == MemberMenuOption.BROWSEAUHTORANDTITLE.value:
        return MemberMenuOption.BROWSEAUHTORANDTITLE
    elif option == MemberMenuOption.CHECKOUT.value:
        return MemberMenuOption.CHECKOUT
    elif option == MemberMenuOption.LOGOUT.value:
        return MemberMenuOption.LOGOUT

def printCartInfo(cartInfo):
    totalPriceCart = 0
    if cartInfo is None or len(cartInfo) == 0:
        print("Cart seems to be empty, might be due to invalid user ID")
        return False
    else:
        print("---------- CURRENT CART CONTENTS: ------------")

        # Print table header
        print("+------------+----------------------------------------------------+-----+---------+")
        print("| ISBN       | Title                                              | Qty | Total   |")
        print("+------------+----------------------------------------------------+-----+---------+")

        # Print table rows
        for item in cartInfo:
            total = item['quantity'] * item['price']
            totalPriceCart += total
            print("| {isbn:<10} | {title:<50} | {quantity:>3} | {total:>7.2f} |".format(
                isbn=item['isbn'],
                title=item['title'][:50],
                quantity=item['quantity'],
                total=total
            ))
            print("+------------+----------------------------------------------------+-----+---------+")

        # Print table footer with total price
        print("| {totalPriceCart:<72} ".format(totalPriceCart=f"Total Price: {totalPriceCart:.2f}"))
        print("+---------------------------------------------------------------------------------+")
        return True

def printOrderInfo(orderNumber):
    # Connect to database
    connection = database.getDatabaseConnection()
    cursor = connection.cursor()
    

    # Define the SQL query
    query = """
        SELECT members.fname, members.lname, members.address, members.city, members.zip,
            odetails.isbn, books.title, odetails.qty, odetails.qty * books.price AS total
        FROM members
        JOIN (
            SELECT odetails.ono, odetails.isbn, odetails.qty, books.price
            FROM odetails
            JOIN books ON odetails.isbn = books.isbn
        ) AS odetails ON members.userid = (
            SELECT orders.userid
            FROM orders
            WHERE orders.ono = odetails.ono
        )
        JOIN books ON odetails.isbn = books.isbn
        WHERE odetails.ono = %s
    """
    params = (orderNumber,)

    # Execute the query and fetch the results
    cursor.execute(query, params)
    results = cursor.fetchall()

    # Get today's date
    today = datetime.date.today()


    # Add one week to today's date
    oneWeek = datetime.timedelta(days=7)
    estDeliveryDate = today + oneWeek

    # Print the output header
    print(f"Invoice for order number: {orderNumber}\n")
    print(f"Estimated delivery date: {estDeliveryDate}\n")
    print("Shipping Address: ")
    print(f"Name: {results[0][0]} {results[0][1]}")
    print(f"Address: {results[0][2]}\n         {results[0][3]}\n         {results[0][4]}\n")

    print("+------------+----------------------------------------------------+-----+---------+")
    print("| ISBN       | Title                                              | Qty | Total   |")
    print("+------------+----------------------------------------------------+-----+---------+")

    # Print the table data
    grandTotal = 0
    for row in results:
        grandTotal += row[8]
        print("| {isbn:<10} | {title:<50} | {qty:>3} | {total:>7.2f} |".format(
            isbn=row[5], title=row[6][:50], qty=row[7], total=row[8]))

    # Print the table footer with grand total price
    print("+------------+----------------------------------------------------+-----+---------+")
    print("| {grandTotal:<64} ".format(grandTotal=f"Grand Total: {grandTotal:.2f}"))
    print("+-----------------------------------------------------------------+-----+---------+")

    # Close database connection
    connection.close()


def printUserIdPrompt():
    while True:
        try:
            userid = int(input("Enter your user ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return userid

def printCheckOutPrompt():

    wantsToCheckOut = input("Proceed to checkout? Y/N: ")

    if wantsToCheckOut.lower() == "y":
      return True
    else:
      return False

