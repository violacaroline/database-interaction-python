import datetime
import random
import database

def getCart(userid):
    # Connect to database
    connection = database.getDatabaseConnection()
    cursor = connection.cursor()

    # Fetch the cart for the specified user
    cursor.execute(
        "SELECT isbn, qty FROM cart WHERE userid = %s",
        (userid,)
    )
    cartItems = cursor.fetchall()

    # Fetch the book information for each item in the cart
    cartInfo = []
    for isbn, qty in cartItems:
        cursor.execute(
            "SELECT isbn, title, price FROM books WHERE isbn = %s",
            (isbn,)
        )
        bookInfo = cursor.fetchone()
        cartInfo.append({
            'isbn': bookInfo[0],
            'title': bookInfo[1],
            'quantity': qty,
            'price': bookInfo[2]
        })

    return cartInfo

def generateOrderNumber():
    return random.randint(100000, 999999)

def placeOrder(userid, cartInfo):
    # Connect to database
    connection = database.getDatabaseConnection()
    cursor = connection.cursor()

    # Get today's date
    today = datetime.date.today()

    # Generate random ONO
    orderNumber = generateOrderNumber()

    # Fetch the member's address, city, state, and zip by their userid
    cursor = connection.cursor()
    cursor.execute("SELECT address, city, state, zip FROM members WHERE userid = %s", (userid,))
    result = cursor.fetchone()

    if result:
        address, city, state, zip = result

        # Insert a new order into the "orders" table with the member's information
        ono = orderNumber
        received = today
        shipped = None
        shipAddress = address
        shipCity = city
        shipState = state
        shipZip = zip

        cursor.execute("INSERT INTO orders (userid, ono, received, shipped, shipAddress, shipCity, shipState, shipZip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (userid, ono, received, shipped, shipAddress, shipCity, shipState, shipZip))
        connection.commit()

        # Insert each item in the cartInfo array into the "odetails" table

        for item in cartInfo:
            isbn = item['isbn']
            qty = item['quantity']
            price = item['price']
            cursor = connection.cursor()
            cursor.execute("INSERT INTO odetails (ono, isbn, qty, price) VALUES (%s, %s, %s, %s)", (ono, isbn, qty, price))
            connection.commit()

        # Empty cart
        cursor.execute("DELETE FROM cart")
        connection.commit()


    # Close database connection
    connection.close()
    return orderNumber
