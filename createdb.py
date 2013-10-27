#!/usr/bin/python2.7
import sqlite3
import json
from collections import defaultdict

def emptyString():
	return ""

db = sqlite3.connect("books.db")
c = db.cursor()

booksFile = open("books.json")
books = json.load(booksFile)
booksFile.close()

columns = []

for book in books.values():
	if "authors" in book:
		book["authors"] = ", ".join(book["authors"])
	for column in book.keys():
		if column not in columns:
			columns.append(column)

insertQuery = "INSERT INTO books values ("+",".join([":"+x for x in columns])+");"

for book in books.values():
	c.execute(insertQuery, defaultdict(emptyString, book))