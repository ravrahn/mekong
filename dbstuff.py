#!/usr/bin/python2.7
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sqlite3.connect("books.db")
db.row_factory = dict_factory
c = db.cursor()
c.execute("SELECT isbn,title,authors FROM books WHERE title LIKE \"%hello%\" LIMIT 5")
print c.fetchall()