#!/usr/bin/python2.7
import sqlite3
import json
from collections import defaultdict

def emptyString():
    return ""

db = sqlite3.connect("books.db")
c = db.cursor()

c.execute("DROP TABLE IF EXISTS books")

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


c.execute('''CREATE TABLE books (isbn text primary key,
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

insertQuery = "INSERT INTO books VALUES ("+",".join([":"+x for x in columns])+");"

for book in books:
    c.execute(insertQuery, defaultdict(emptyString, book))
    db.commit()