import sqlite3
import random

def dict_factory(cursor, row):
    '''
    A helper function for sqlite3 that allows rows
    to be returned as dictionaries
    '''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getBooks():
    '''
    returns a list of every book in the database
    '''
    db = sqlite3.connect("books.db")
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute("SELECT * FROM books")

    books = []
    for book in c:
        books.append(book)
    return books

def searchBooks(searchString, category="title"):
    '''
    returns a list of Book objects matching a search searchString
    '''
    db = sqlite3.connect("books.db")
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute("SELECT isbn,title,authors,price,largeimageurl FROM books WHERE title LIKE \"%"+searchString+"%\"")

    books = c.fetchall()

    return books

def featuredBooks():
    '''
    returns a few featured books
    '''


def topBooks(amount=10):
    '''
    returns the top books by salesrank
    '''
    db = sqlite3.connect("books.db")
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute("SELECT isbn,title,authors,price,largeimageurl,salesrank FROM books ORDER BY salesrank LIMIT "+str(amount))

    books = c.fetchall()

    return books

def bookDetails(isbn):
    '''
    returns information about one book
    for use on the book-detail page
    '''
    db = sqlite3.connect("books.db")
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute("SELECT isbn,title,authors,price,largeimageurl,productdescription FROM books WHERE isbn = \""+isbn+"\"")

    return c.fetchone()
