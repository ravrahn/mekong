#!/usr/bin/python2.7
import sqlite3

db = sqlite3.connect("users.db")
c = db.cursor()

c.execute("DROP TABLE IF EXISTS users")
c.execute("DROP TABLE IF EXISTS sessions")

c.execute("""CREATE TABLE users (
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

c.execute("""CREATE TABLE sessions (
				sessionid TEXT PRIMARY KEY,
				username TEXT
			);""")

db.commit()