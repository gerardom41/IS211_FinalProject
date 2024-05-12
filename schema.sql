DROP TABLE IF EXISTS books;

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT,
    book_author TEXT,
    book_page INTEGER,
    book_rating TEXT
);
