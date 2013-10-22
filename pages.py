def getHeader(searchTerms=""):
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

	return header % {"username": username}

def login():
	loginFile = open("login.html", "r")
	login = loginFile.read()
	loginFile.close()

	return login % {"header":getHeader()}

def landing():
	landingFile = open("landing.html", "r")
	landing = landingFile.read()
	landingFile.close()

	return landing

def index():
	indexFile = open("index.html", "r")
	index = indexFile.read()
	indexFile.close()

	return index

def mekong(title):
	mekongFile = open("mekong.html", "r")
	mekong = mekongFile.read()
	mekongFile.close()

	return mekong % {"title":title, "header":getHeader()}