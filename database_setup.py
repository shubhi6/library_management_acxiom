import sqlite3

def setup_database():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Create books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)

    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            issue_date DATE NOT NULL,
            return_date DATE,
            fine REAL DEFAULT 0.0,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Insert default users
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "admin123", "admin"))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("user", "user123", "user"))
    except sqlite3.IntegrityError:
        pass  # Skip if already inserted

    connection.commit()
    connection.close()
# Function to add a book
def add_book(title, author, category, available=1):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    
    # Check if the book already exists in the database
    cursor.execute("SELECT * FROM books WHERE title = ? AND author = ?", (title, author))
    existing_book = cursor.fetchone()
    
    if existing_book:
        print(f"Book '{title}' by {author} already exists in the database.")
    else:
        cursor.execute("""
            INSERT INTO books (title, author, category, available) 
            VALUES (?, ?, ?, ?)
        """, (title, author, category, available))

        connection.commit()
        print(f"Book '{title}' added successfully.")

    connection.close()

# Function to remove a book and reset the auto-increment ID
def remove_book(book_id):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    # Check if the book exists before removing
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    
    if book:
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        connection.commit()

        # Reset auto-increment ID for books table
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='books'")
        connection.commit()

        print(f"Book with ID {book_id} removed successfully.")
    else:
        print(f"Book with ID {book_id} does not exist.")
    
    connection.close()

# Function to add a user
def add_user(username, password, role):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, password, role) 
            VALUES (?, ?, ?)
        """, (username, password, role))

        connection.commit()
        print(f"User '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists.")

    connection.close()

# Function to remove a user
def remove_user(user_id):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    
    connection.commit()
    connection.close()
    print(f"User with ID {user_id} removed successfully.")
# Function to display all users
def display_users():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    print("Users in the database:")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[3]}")

    connection.close()
# Function to display all books
def display_books():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    print("Books in the database:")
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Category: {book[3]}, Available: {book[4]}")

    connection.close()

if __name__ == "__main__":
    setup_database()
    
    
