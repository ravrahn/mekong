import sqlite3
import json
from collections import defaultdict
import os


def createDatabases():
    
    if not os.path.isfile("users.db"):
        createUsersDB()

    if not os.path.isfile("books.db"):
        createBooksDB()



def emptyString():
    return ""

def createBooksDB():
    db = sqlite3.connect("books.db")
    c = db.cursor()

    booksFile = open("books.json")
    booksTemp = json.load(booksFile)
    booksFile.close()

    columns = []

    books = []

    for book in booksTemp.values():
        if "authors" in book:
            book["authors"] = ", ".join(book["authors"])
        if "salesrank" in book:
            book["salesrank"] = int(book["salesrank"])
        else:
            book["salesrank"] = 10000000000; # like a billion
        books.append(book)
        for column in book.keys():
            if column not in columns:
                columns.append(column)


    c.execute('''CREATE TABLE IF NOT EXISTS books (isbn text primary key,
        year text,
        binding text,
        mediumimageurl text,
        smallimagewidth text,
        largeimagewidth text,
        title text,
        smallimageheight text,
        salesrank int,
        price text,
        numpages text,
        largeimageurl text,
        productdescription text,
        ean text,
        smallimageurl text,
        catalog text,
        authors text,
        publication_date text,
        mediumimageheight text,
        publisher text,
        largeimageheight text,
        mediumimagewidth text,
        releasedate text,
        edition text
    );''')

    insertQuery = "INSERT OR IGNORE INTO books VALUES ("+",".join([":"+x for x in columns])+");"

    for book in books:
        c.execute(insertQuery, defaultdict(emptyString, book))
        db.commit()

def createUsersDB():
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    firstname TEXT,
                    lastname TEXT,
                    email TEXT,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    postcode INTEGER,
                    validated BOOLEAN
                );""");

    c.execute("""CREATE TABLE IF NOT EXISTS sessions (
                    sessionid TEXT PRIMARY KEY,
                    username TEXT
                );""")

    c.execute("""CREATE TABLE IF NOT EXISTS carts (
                    username TEXT,
                    isbn TEXT,
                    quantity INTEGER
                );""")

    c.execute("""CREATE TABLE IF NOT EXISTS orders (
                    username TEXT,
                    isbn TEXT,
                    quantity INTEGER
                );""")

    db.commit()