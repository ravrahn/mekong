import sqlite3
import hashlib
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def hashUser(username):
    db = sqlite3.connect("users.db")
    c = db.cursor()

    c.execute("SELECT uuid FROM users WHERE username = \""+username+"\"")

    userid = c.fetchone()

    return hashlib.md5(str(userid)).hexdigest()

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
        "postcode",
        "validated"
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

    

    c.execute("SELECT uuid,username FROM users")

    for uuid,username in c.fetchall():
        if hashUser(username) == userHash:
            c.execute("UPDATE users SET validated=1 WHERE uuid="+str(uuid))
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

    results = results[0]

    passwordHash = hashlib.md5(passwordText).hexdigest()

    if results == passwordHash:
        return True
    else:
        return False

