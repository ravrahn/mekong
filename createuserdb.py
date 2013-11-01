#!/usr/bin/python2.7
import sqlite3

db = sqlite3.connect("users.db")
c = db.cursor()

c.execute("DROP TABLE IF EXISTS users")

c.execute("""CREATE TABLE users (
				uuid INTEGER PRIMARY KEY AUTOINCREMENT,
				username TEXT,
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

db.commit()