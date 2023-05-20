import database
import mysql.connector


def browseSubjects():
# Connect to database
  connection = database.getDatabaseConnection()
  cursor = connection.cursor()

  # Query the database for all subjects
  cursor.execute("SELECT DISTINCT subject FROM books ORDER BY subject")
  subjects = [row[0] for row in cursor.fetchall()]

  # Display the list of subjects and allow the user to choose one
  print("===================================")
  print("         AVAILABLE SUBJECTS")
  print("===================================")
  for i, subject in enumerate(subjects):
      print(f"[{i+1}] {subject}")
  print("===================================")
  while True:
        subjectOption = input("Enter the number of the subject you would like to browse: ")
        try:
            subjectOption = int(subjectOption)
            if subjectOption < 1 or subjectOption > 8:
                print("Invalid input. Please enter a number between 1 and 8.")
            else:
                subject = subjects[subjectOption-1]
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

  cursor.execute("SELECT COUNT(*) FROM books WHERE subject = %s", (subject,))
  amountBooksInSubject = cursor.fetchone()[0]
  print(f"There are {amountBooksInSubject} books in the {subject} subject.")

  cursor.execute("SELECT * FROM books WHERE subject = %s ORDER BY title", (subject,))
  books = cursor.fetchall()

  # Display the books two at a time
  i = 0
  while i < len(books):
      print("===================================")
      print(f"BOOKS IN {subject.upper()}")
      print("===================================")
      for j in range(i, min(i+2, len(books))):
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
                    print("Error: Could not add book to cart. Please check your user ID.")
                    connection.rollback()
      elif action == 'n':
          i += 2
          continue
      else:
          break

  # Close database connection
  connection.close()





