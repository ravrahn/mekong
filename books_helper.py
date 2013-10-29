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

def getBook(isbn):
    '''
    returns a single book dictionary from the database
    '''
    db = sqlite3.connect("books.db")
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute("""SELECT isbn,
                        title,
                        authors,
                        releasedate,
                        publisher,
                        salesrank,
                        largeimageurl,
                        productdescription,
                        price
                    FROM books
                    WHERE isbn = ?""", (isbn,))

    return c.fetchone()

def searchBooks(queryString, category):
    '''
    returns a list of book dictionaries objects matching a search searchString
    '''
    db = sqlite3.connect("books.db")
    db.row_factory = dict_factory
    c = db.cursor()

    if category == "all":
        query = """SELECT isbn,title,authors,price,largeimageurl,salesrank
                        ,(CASE WHEN isbn LIKE '%' || ? || '%' THEN 3 ELSE 0 END) +
                        (CASE WHEN authors LIKE '%' || ? || '%' THEN 2 ELSE 0 END) +
                        (CASE WHEN title LIKE '%' || ? || '%' THEN 2 ELSE 0 END) +
                        (CASE WHEN productdescription LIKE '%' || ? || '%' THEN 1 ELSE 0 END) AS [priority]
                    FROM books
                    WHERE isbn LIKE '%' || ? || '%'
                        OR title LIKE '%' || ? || '%'
                        OR authors LIKE '%' || ? || '%'
                        OR productdescription LIKE '%' || ? || '%'
                    ORDER BY [priority] DESC, salesrank"""
        c.execute(query, (queryString,) * 8)
    elif category == "title":
        query = """SELECT isbn,title,authors,price,largeimageurl,salesrank
                    FROM books
                    WHERE title LIKE '%' || ? || '%'
                    ORDER BY salesrank""" 
        c.execute(query, (queryString,))
    elif category == "authors":
        query = """SELECT isbn,title,authors,price,largeimageurl,salesrank
                    FROM books
                    WHERE authors LIKE '%' || ? || '%'
                    ORDER BY salesrank""" 
        c.execute(query, (queryString,))
    elif category == "isbn":
        query = """SELECT isbn,title,authors,price,largeimageurl,salesrank
                    FROM books
                    WHERE isbn LIKE '%' || ? || '%'
                    ORDER BY salesrank""" 
        c.execute(query, (queryString,))
    elif category == "productdescription":
        query = """SELECT isbn,title,authors,price,largeimageurl,salesrank
                    FROM books
                    WHERE productdescription LIKE '%' || ? || '%'
                    ORDER BY salesrank""" 
        c.execute(query, (queryString,))

    books = c.fetchall()
    return books
    

    


def featuredBooks():
    '''
    returns a few featured books
    '''
    db = sqlite3.connect("books.db")
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute("SELECT isbn,title,authors,price,largeimageurl,salesrank FROM books ORDER BY RANDOM() LIMIT 6")

    books = c.fetchall()

    return books

def topBooks(amount=6):
    '''
    returns the top books by salesrank
    '''
    db = sqlite3.connect("books.db")
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute("SELECT isbn,title,authors,price,largeimageurl,salesrank FROM books ORDER BY salesrank LIMIT "+str(amount))

    books = c.fetchall()

    for book in books:
        book["title"] = str(book.get("salesrank"))+". "+book.get("title")

    return books

def bookDetails(isbn):
    '''
    returns information about one book
    for use on the book-detail page
    '''
    db = sqlite3.connect("books.db")
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute("SELECT isbn,title,authors,price,largeimageurl,productdescription,salesrank FROM books WHERE isbn = \""+isbn+"\"")

    return c.fetchone()
