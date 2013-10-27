import json
import random

def getBooks():
	'''
	returns a list of Book objects for every book in books.json
	'''
	booksFile = open("books.json", "r")
	books = []
	for bookDict in json.load(booksFile).values():
		books.append(bookDict)
	booksFile.close()
	return books

def getBook(isbn):
	'''
	returns a Book object for a specific isbn
	'''
	booksFile = open("books.json", "r")
	book = Book(json.load(booksFile)[isbn])
	booksFile.close()
	
	return book

def searchBooks(searchString, category="title"):
	'''
	returns a list of Book objects matching a search searchString
	'''
	allBooks = getBooks()
	random.shuffle(allBooks)
	books = allBooks[:50]

	return books

def featuredBooks():
	'''
	returns a few featured books
	'''
	allBooks = getBooks()
	topBooks = sorted(allBooks, key=lambda k: k.get("salesrank", 10000000))[:100]
	random.shuffle(topBooks)
	books = topBooks[:5]
	return books
