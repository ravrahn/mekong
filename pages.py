from books_helper import *

def getHeader(query=""):
	'''
	in future, will check if user is logged in, etc.
	'''
	username = "Login or Register"
	headerSrc = "header.html"

	# if user is logged in.
	# then use the logged-in header
	# comment in haiku

	headerFile = open(headerSrc, "r")
	header = headerFile.read()
	headerFile.close()

	return header % { "username": username, "query": query }

def login():
	# load the login html
	# and return it as a string
	loginFile = open("login.html", "r")
	login = loginFile.read()
	loginFile.close()

	return login % { "header":getHeader() }

def search(query):
	searchFile = open("search.html", "r")
	search = searchFile.read()
	searchFile.close()

	resultFile = open("result.html", "r")
	result = resultFile.read()
	resultFile.close()

	books = searchBooks(query)

	string = ""
	for book in books:
		string += result % { "isbn": book.get("isbn"), "imgsrc": book.get("largeimageurl"), "title": book.get("title"), "author": ", ".join(book.get("authors")), "price": book.get("price"), "rank": book.get("salesrank") }

	return search % { "header":getHeader(query=query), "query": query, "numResults": str(len(books)) , "results": string }

def mekong(title):
	mekongFile = open("mekong.html", "r")
	mekong = mekongFile.read()
	mekongFile.close()

	resultFile = open("result.html", "r")
	result = resultFile.read()
	resultFile.close()

	books = featuredBooks()

	string = ""
	for book in books:
		string += result % { "isbn": book.get("isbn"), "imgsrc": book.get("largeimageurl"), "title": book.get("title"), "author": ", ".join(book.get("authors")), "price": book.get("price"), "rank": book.get("salesrank") }

	return mekong % { "header":getHeader(), "featured": string }

