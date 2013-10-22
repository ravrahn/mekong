import json

class Book(object):
	def __init__(self, bookDict):
		if "isbn" in bookDict:
		    self.isbn = bookDict["isbn"]
		else:
		    self.isbn = None

		if "ean" in bookDict:
		    self.ean = bookDict["ean"]
		else:
		    self.ean = None

		if "largeimageurl" in bookDict:
		    self.largeimageurl = bookDict["largeimageurl"]
		else:
		    self.largeimageurl = None

		if "catalog" in bookDict:
		    self.catalog = bookDict["catalog"]
		else:
		    self.catalog = None

		if "binding" in bookDict:
		    self.binding = bookDict["binding"]
		else:
		    self.binding = None

		if "numpages" in bookDict:
		    self.numpages = bookDict["numpages"]
		else:
		    self.numpages = None

		if "smallimageurl" in bookDict:
		    self.smallimageurl = bookDict["smallimageurl"]
		else:
		    self.smallimageurl = None

		if "mediumimagewidth" in bookDict:
		    self.mediumimagewidth = bookDict["mediumimagewidth"]
		else:
		    self.mediumimagewidth = None

		if "publication_date" in bookDict:
		    self.publication_date = bookDict["publication_date"]
		else:
		    self.publication_date = None

		if "productdescription" in bookDict:
		    self.productdescription = bookDict["productdescription"]
		else:
		    self.productdescription = None

		if "publisher" in bookDict:
		    self.publisher = bookDict["publisher"]
		else:
		    self.publisher = None

		if "releasedate" in bookDict:
		    self.releasedate = bookDict["releasedate"]
		else:
		    self.releasedate = None

		if "authors" in bookDict:
		    self.authors = bookDict["authors"]
		else:
		    self.authors = None

		if "largeimageheight" in bookDict:
		    self.largeimageheight = bookDict["largeimageheight"]
		else:
		    self.largeimageheight = None

		if "mediumimageheight" in bookDict:
		    self.mediumimageheight = bookDict["mediumimageheight"]
		else:
		    self.mediumimageheight = None

		if "mediumimageurl" in bookDict:
		    self.mediumimageurl = bookDict["mediumimageurl"]
		else:
		    self.mediumimageurl = None

		if "largeimagewidth" in bookDict:
		    self.largeimagewidth = bookDict["largeimagewidth"]
		else:
		    self.largeimagewidth = None

		if "salesrank" in bookDict:
		    self.salesrank = bookDict["salesrank"]
		else:
		    self.salesrank = None

		if "smallimageheight" in bookDict:
		    self.smallimageheight = bookDict["smallimageheight"]
		else:
		    self.smallimageheight = None

		if "smallimagewidth" in bookDict:
		    self.smallimagewidth = bookDict["smallimagewidth"]
		else:
		    self.smallimagewidth = None

		if "price" in bookDict:
		    self.price = bookDict["price"]
		else:
		    self.price = None

		if "title" in bookDict:
		    self.title = bookDict["title"]
		else:
		    self.title = None

		if "year" in bookDict:
		    self.year = bookDict["year"]
		else:
		    self.year = None


def getBooks():
	'''
	returns a list of Book objects for every book in books.json
	'''
	booksFile = open("books.json", "r")
	books = []
	for bookDict in json.load(booksFile).values():
		books.append(Book(bookDict))
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
	books = getBooks()
