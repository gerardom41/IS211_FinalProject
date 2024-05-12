from flask import Flask, render_template, request, redirect, url_for, flash, session # type: ignore
import sqlite3
import re
import requests # type: ignore

app = Flask(__name__)
app.secret_key = "Not_so_secret_key_final"

#home redirects to login page
@app.route("/")
def home():
    return redirect(url_for("login"))

#Use admin and password
@app.route("/login" , methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "password":
            session["logged_in"] = True
            return redirect(url_for("book_catalogue"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")

@app.route("/book_catalogue")
def book_catalogue():
    if "logged_in" not in session:
        return redirect(url_for("login"))
    conn, cursor = connect_to_db()
    books = read_data(cursor, "books")
    conn.close()
    return render_template("book_catalogue.html", books=books)

def get_book(isbn):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    input = {"q": f"isbn:{isbn}"}
    try:
        response = requests.get(base_url, params=input)
        response.raise_for_status()
        book_data_all = response.json()
        book_info = book_data_all["items"][0]["volumeInfo"]
    except (requests.RequestException, KeyError, IndexError, TypeError) as e:
        flash(f"Error: {e}")
    else:
        title = book_info["title"]
        authors = book_info["authors"]
        page_count = book_info["pageCount"]
        average_rating = book_info.get("averageRating")

        return {
            "title": title,
            "authors": authors,
            "page_count": page_count,
            "average_rating": average_rating,
        }

@app.route("/book/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_id = count_items_table("books") + 1
        book_isbn = request.form.get("book_isbn")
        book_regexp = re.compile(r"^\d{13}$")
        if book_regexp.match(book_isbn):
            book = get_book(book_isbn)
            authors = ", ".join(book["authors"])
            conn, cursor = connect_to_db()
            cursor.execute("INSERT INTO books (book_id, book_title, book_author, book_page, book_rating) VALUES (?, ?, ?, ?, ?)",
            (book_id, book["title"], authors, book["page_count"], book["average_rating"]))
            close_connection(conn)
        else:
            flash("Invalid ISBN")
        return redirect(url_for("book_catalogue"))
    return render_template("book_catalogue.html")

@app.route("/book/delete", methods=["GET", "POST"])
def delete_book():
    if request.method == "POST":
        delete_book = request.form.get("delete_book")
        conn, cursor = connect_to_db()
        cursor.execute("DELETE FROM books WHERE book_title LIKE ?", (delete_book,))
        close_connection(conn)
        return redirect(url_for("book_catalogue"))
    return render_template("book_catalogue.html")

def connect_to_db():
    conn = sqlite3.connect("book_catalogue.db")
    cursor = conn.cursor()
    return conn, cursor

def create_tables(cursor):
    with open("schema.sql", "r") as f:
        sqlite = f.read()
    cursor.executescript(sqlite)

def clear_tables(cursor):
    cursor.execute("DELETE FROM books")

def count_items_table(table):
    conn, cursor = connect_to_db()
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    close_connection(conn)
    return count

def read_data(cursor, table):
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()

def close_connection(conn):
    conn.commit()
    conn.close()

def start_db():
    conn, cursor = connect_to_db()
    create_tables(cursor)
    clear_tables(cursor)
    close_connection(conn)

if __name__ == "__main__":
    start_db()
    app.run()
