import database
import mysql.connector

def browseAuthorsAndTitles():
    # Connect to database
    connection = database.getDatabaseConnection()
    cursor = connection.cursor()

    while True:
        print("Please choose an option:")
        print("1. Author Search")
        print("2. Title Search")
        print("3. Go Back to Member Menu")
        choice = input("Select an option: ")

        if choice == "1":
            searchString = input("Enter a substring to search for in author names: ")
            query = "SELECT * FROM books WHERE author LIKE %s"
            params = ('%' + searchString + '%',)
        elif choice == "2":
            searchString = input("Enter a substring to search for in book titles: ")
            query = "SELECT * FROM books WHERE title LIKE %s"
            params = ('%' + searchString + '%',)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        cursor.execute(query, params)
        books = cursor.fetchall()

        # Display the books three at a time
        i = 0
        while i < len(books):
            print("===================================")
            print(f"BOOKS SEARCHED FOR: {searchString}")
            print("===================================")
            for j in range(i, min(i+3, len(books))):
                print(f"ISBN: {books[j][0]}")
                print(f"Author: {books[j][1]}")
                print(f"Title: {books[j][2]}")
                print(f"Price: {books[j][3]}")
            print("===================================")
            action = input('Press "A" to Add to cart, "N" to see next page, or press ENTER to return to menu: ')
            if action == 'a':
                # Add book to cart
                # Get the user input
                while True:
                    try:
                        userId = int(input("Enter your user ID: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")                
                isbn = input("Enter the ISBN of the book: ")
                quantity = input("Enter the quantity of books: ")

                # Query the database to check if the book exists
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
                book = cursor.fetchone()

                if book is None:
                    print("Error: Book not found.")
                else:
                    # Insert the book into the cart table
                    try:
                        cursor.execute("INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s)", (userId, isbn, quantity))
                        connection.commit()
                        print(f"{quantity} copies of {book[1]} have been added to your cart.")
                    except mysql.connector.errors.DatabaseError:
                        print("Error: Could not add book to cart. Please check your input.")
                        connection.rollback()
            elif action == 'n':
                i += 3
                continue
            else:
                break

    # Close database connection
    connection.close()
