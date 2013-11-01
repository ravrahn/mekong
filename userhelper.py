import sqlite3
import hashlib

def addUser(user):
	columns = [
		"uuid",
		"username",
		"password",
		"firstname",
		"lastname",
		"email",
		"address",
		"city",
		"state",
		"postcode"
	]

	db = sqlite3.connect("users.db")
	c = db.cursor()

	# if any of the text has not been entered
	if ("username" not in user or
		"password" not in user or
		"firstname" not in user or
		"lastname" not in user or
		"email" not in user or
		"address" not in user or
		"city" not in user or
		"state" not in user or
		"postcode" not in user):
		print "<!-- "
		print user
		print " -->"
		return False

	c.execute("SELECT username FROM users WHERE username = \""+user["username"]+"\"")

	if len(c.fetchall()) > 0:
		return False

	user["uuid"] = None

	passwordHash = hashlib.md5(user["password"]).hexdigest()
	user["password"] = passwordHash

	insertQuery = "INSERT INTO users VALUES ("+",".join([":"+x for x in columns])+");"

	c.execute(insertQuery, user)
	db.commit()

	return True


