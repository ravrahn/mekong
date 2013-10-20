def login():
	loginFile = open("login.html", "r")
	login = loginFile.read()
	loginFile.close()

	return login

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