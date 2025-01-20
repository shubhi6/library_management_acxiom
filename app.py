from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # Add database logic here
    if username == "admin" and password == "admin123":
        return redirect(url_for("admin_dashboard"))
    elif username == "user" and password == "user123":
        return redirect(url_for("user_dashboard"))
    else:
        flash("Invalid credentials")
        return redirect(url_for("home"))

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/user_dashboard")
def user_dashboard():
    return render_template("user_dashboard.html")

# Route to list all books
@app.route("/master_list_books")
def master_list_books():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all books from the database
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    connection.close()

    return render_template("master_list_books.html", books=books)

# Route to add a book
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        available = int(request.form["available"])

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO books (title, author, category, available)
            VALUES (?, ?, ?, ?)
        """, (title, author, category, available))
        connection.commit()
        connection.close()

        flash("Book added successfully!")
        return redirect(url_for("master_list_books"))

    return render_template("add_book.html")

# Route to update book details
@app.route("/update_book", methods=["GET", "POST"])
def update_book():
    if request.method == "POST":
        book_id = request.form["book_id"]
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        available = int(request.form["available"])

        connection = get_db_connection()
        cursor = connection.cursor()

        # Update book details
        cursor.execute("""
            UPDATE books
            SET title = ?, author = ?, category = ?, available = ?
            WHERE id = ?
        """, (title, author, category, available, book_id))
        connection.commit()
        connection.close()

        flash("Book updated successfully!")
        return redirect(url_for("master_list_books"))

    return render_template("update_book.html")

@app.route("/active_issues")
def active_issues():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch active book issues (transactions where return_date is NULL)
    cursor.execute("""
        SELECT t.id, b.title, u.username, t.issue_date
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        JOIN users u ON t.user_id = u.id
        WHERE t.return_date IS NULL
    """)
    active_transactions = cursor.fetchall()

    connection.close()

    return render_template("active_issues.html", transactions=active_transactions)
from datetime import datetime

@app.route("/overdue_returns")
def overdue_returns():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Fetch overdue returns (transactions where return_date is NULL and the issue_date is older than current date)
    cursor.execute("""
        SELECT t.id, b.title, u.username, t.issue_date
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        JOIN users u ON t.user_id = u.id
        WHERE t.return_date IS NULL AND t.issue_date < ?
    """, (current_date,))
    overdue_transactions = cursor.fetchall()

    connection.close()

    return render_template("overdue_returns.html", transactions=overdue_transactions)
@app.route("/master_list_members")
def master_list_members():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all members (users)
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()

    connection.close()

    return render_template("master_list_members.html", users=users)
@app.route("/return_book", methods=["GET", "POST"])
def return_book():
    if request.method == "POST":
        user_id = request.form["user_id"]
        book_id = request.form["book_id"]
        return_date = request.form["return_date"]

        connection = get_db_connection()
        cursor = connection.cursor()

        # Check for active transaction
        cursor.execute("""
            SELECT id FROM transactions
            WHERE book_id = ? AND user_id = ? AND return_date IS NULL
        """, (book_id, user_id))
        transaction = cursor.fetchone()

        if transaction:
            # Update transaction and increment available count
            cursor.execute("UPDATE transactions SET return_date = ? WHERE id = ?", (return_date, transaction["id"]))
            cursor.execute("UPDATE books SET available = available + 1 WHERE id = ?", (book_id,))
            connection.commit()
            flash("Book returned successfully!")
        else:
            flash("No active issue record found!")

        connection.close()
        return redirect(url_for("search_books"))

    return render_template("return_book.html")
@app.route("/issue_book", methods=["GET", "POST"])
def issue_book():
    if request.method == "POST":
        user_id = request.form["user_id"]
        book_id = request.form["book_id"]
        issue_date = request.form["issue_date"]

        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the book is available
        cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()

        if book and book["available"] > 0:
            # Reduce the book's available count and add transaction
            cursor.execute("UPDATE books SET available = available - 1 WHERE id = ?", (book_id,))
            cursor.execute("""
                INSERT INTO transactions (book_id, user_id, issue_date)
                VALUES (?, ?, ?)
            """, (book_id, user_id, issue_date))
            connection.commit()
            flash("Book issued successfully!")
        else:
            flash("Book is not available!")

        connection.close()
        return redirect(url_for("search_books"))

    return render_template("issue_book.html")
@app.route("/search_books", methods=["GET", "POST"])
def search_books():
    books = []
    if request.method == "POST":
        search_query = request.form["search_query"]
        
        connection = get_db_connection()
        cursor = connection.cursor()

        # Search for books by title, author, or category
        cursor.execute("""
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR category LIKE ?
        """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
        books = cursor.fetchall()

        connection.close()

    return render_template("search_books.html", books=books)

if __name__ == "__main__":
    app.run(debug=True)
