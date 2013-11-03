# for accessing the databases
import sqlite3
# for hashing passwords
import hashlib
# for sending emails
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
# for managing sessions
import Cookie
import uuid
import os
# for cart stuff
import bookhelper


def hashUser(username):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT password FROM users WHERE username = \""+username+"\"")

    password, = c.fetchone()

    return hashlib.md5(password+username).hexdigest()

def addUser(user):
    columns = [
        "username",
        "password",
        "firstname",
        "lastname",
        "email",
        "address",
        "city",
        "state",
        "postcode",
        "validated"
    ]

    db = sqlite3.connect("users.db")
    c = db.cursor()

    # if any of the text has not been entered
    if ("username" not in user or user["username"] == "" or
        "password" not in user or user["password"] == "" or
        "firstname" not in user or user["firstname"] == "" or
        "lastname" not in user or user["lastname"] == "" or
        "email" not in user or user["email"] == "" or
        "address" not in user or user["address"] == "" or
        "city" not in user or user["city"] == "" or
        "state" not in user or user["state"] == "" or
        "postcode" not in user or user["postcode"] == ""):
        return False

    c.execute("SELECT username FROM users WHERE username = \""+user["username"]+"\"")

    if len(c.fetchall()) > 0:
        return False

    user["validated"] = False

    passwordHash = hashlib.md5(user["password"]).hexdigest()
    user["password"] = passwordHash

    insertQuery = "INSERT INTO users VALUES ("+",".join([":"+x for x in columns])+");"

    c.execute(insertQuery, user)
    db.commit()

    return True

def sendValidationEmail(username, email):
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login("mekong.com.au@gmail.com", "mekongasdf") # shh it's secret

    url = "http://cgi.cse.unsw.edu.au/~obca109/mekong/mekong.cgi?page=validate&user="+hashUser(username)

    htmlContent = """<html>
    <head></head>
    <body>
        Hello!<br >
        <br >
        A Mekong account called "%(username)s" has been created with this email address.<br >
        <br >
        If it's your account, we'd like you to verify it. <a href="%(url)s">Click here</a> or go to the address below and we'll verify your account.<br >
        <br >
        %(url)s<br >
        <br>
        If it's not your account, or you made it by mistake. If you don't validate this account within a week we'll delete it automatically.<br >
        <br >
        Thanks for creating a Mekong account!
    </body>
</html>""" % { "url": url, "username": username }

    msg = MIMEMultipart()
    msg["Subject"] = "You made an account with Mekong"
    msg["From"] = "mekong.com.au@gmail.com"
    msg["To"] = email

    msg.attach(MIMEText(htmlContent, "html"))

    mailServer.sendmail("mekong.com.au@gmail.com", email, msg.as_string())

def validateUser(userHash):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT username FROM users")

    for username, in c.fetchall():
        if hashUser(username) == userHash:
            c.execute("UPDATE users SET validated=1 WHERE username=?", (username,))
            db.commit()
            return True

    return False

def isCorrectPassword(username, passwordText):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT password FROM users WHERE username = \""+username+"\"")

    results = c.fetchall()

    if len(results) != 1:
        return False

    results, = results[0]

    passwordHash = hashlib.md5(passwordText).hexdigest()

    if results == passwordHash:
        return True
    else:
        return False

def getRealName(username):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT firstname,lastname FROM users WHERE username = ?", (username,))

    firstname,lastname = c.fetchone()

    return firstname+" "+lastname



def getSessionId(username):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT sessionid FROM sessions WHERE username = ?", (username,))
    currentSessions = c.fetchall()

    if len(currentSessions) > 0:
        sessionid, = currentSessions[0]
    else:
        sessionid = str(uuid.uuid4()) # so random
        c.execute("INSERT INTO sessions (sessionid, username) VALUES(?, ?);", (sessionid, username))
        db.commit()

    return sessionid

def getUsername(sessionid):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    if sessionid == None:
        return None

    c.execute("SELECT username FROM sessions WHERE sessionid=\""+sessionid+"\"")
    currentUsers = c.fetchall()

    if len(currentUsers) > 0:
        currentUser, = currentUsers[0]
        return currentUser
    else:
        return None

def getCurrentUser():
    cookie = Cookie.SimpleCookie(os.getenv("HTTP_COOKIE"))

    if cookie.has_key("sessionid"):
        currentSession = cookie["sessionid"].value
        return getUsername(currentSession)
    else:
        return None

def loggedInAs(username):
    if getCurrentUser() == username:
        return True
    else:
        return False


def isLoggedIn():
    cookie = Cookie.SimpleCookie(os.getenv("HTTP_COOKIE"))

    if cookie.has_key("sessionid"):
        return True
    else:
        return False

def createSessionCookie(username):
    cookie = Cookie.SimpleCookie()

    cookie["sessionid"] = getSessionId(username)

    return cookie.output()

def logOut(username):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("DELETE FROM sessions WHERE username = ?", (username,))
    db.commit()



def setQuantity(username, isbn, quantity):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("UPDATE carts SET quantity = ? WHERE username = ? AND isbn = ?", (quantity, username, isbn))
    db.commit()

def addToCart(username, isbn, quantity):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    # check if the book is already in the cart
    c.execute("SELECT quantity FROM carts WHERE username = ? AND isbn = ?", (username, isbn))
    books = c.fetchall()
    if len(books) > 0:
        book, = books[0]
        if book < quantity:
            c.execute("UPDATE carts SET quantity = ? WHERE username = ? AND isbn = ?", (quantity, username, isbn))
    else:
        c.execute("INSERT INTO carts (username, isbn, quantity) VALUES (?, ?, ?)", (username, isbn, quantity))
    db.commit()

def removeFromCart(username, isbn):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("DELETE FROM carts WHERE username = ? AND isbn = ?", (username, isbn))
    db.commit()

def getCart(username):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT isbn,quantity FROM carts WHERE username = ?", (username,))

    books = []

    for isbn, quantity in c.fetchall():
        book = bookhelper.getBook(isbn)
        book["quantity"] = quantity
        books.append(book)

    return books

def getCartPrice(username):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT isbn,quantity FROM carts WHERE username = ?", (username,))

    price = 0.0

    for isbn, quantity in c.fetchall():
        book = bookhelper.getBook(isbn)
        bookPrice = float(book["price"][1:])
        price += bookPrice*quantity

    if price == 0:
        return  ""

    return "${0:.2f}".format(round(price,2))

def getOrders(username):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT isbn,quantity FROM orders WHERE username = ?", (username,))

    books = []

    for isbn, quantity in c.fetchall():
        book = bookhelper.getBook(isbn)
        book["quantity"] = quantity
        books.append(book)

    return books

def getOrdersPrice(username):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT isbn,quantity FROM orders WHERE username = ?", (username,))

    price = 0.0

    for isbn, quantity in c.fetchall():
        book = bookhelper.getBook(isbn)
        bookPrice = float(book["price"][1:])
        price += bookPrice*quantity

    if price == 0:
        return  ""

    return "${0:.2f}".format(round(price,2))

def checkout(username, creditCard, password):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT isbn,quantity FROM carts WHERE username = ?;", (username,))

    orders = c.fetchall()

    c.execute("DELETE FROM carts WHERE username = ?;", (username,))

    db.commit()

    for isbn,quantity in orders:
        c.execute("SELECT quantity FROM orders WHERE username = ? AND isbn = ?;", (username,isbn))
        currentOrder = c.fetchone()
        if currentOrder == None:
            c.execute("INSERT INTO orders (username, isbn, quantity) VALUES (?, ?, ?);", (username,isbn,quantity))
        else:
            currentOrder, = currentOrder
            c.execute("UPDATE orders SET quantity = ? WHERE username = ? AND isbn = ?", (quantity+currentOrder, username, isbn))

    db.commit()