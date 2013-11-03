#!/usr/bin/python2.7
import os,re,cgi,cgitb
import userhelper
import pages

cgitb.enable()

form = cgi.FieldStorage()

def http_header(cookie):
    if cookie != None:
        return """Content-Type: text/html
%s
""" % cookie
    else:
        return """Content-Type: text/html
"""

notification = ""

cookieSet = None

# 
# USER STUFF
# 
if "action" in form and "Create Account" in form.getlist("action"):
    # make a user dictionary
    user = {}
    user["username"] = form.getfirst("username")
    user["password"] = form.getfirst("password")
    user["firstname"] = form.getfirst("firstname")
    user["lastname"] = form.getfirst("lastname")
    user["email"] = form.getfirst("email")
    user["address"] = form.getfirst("address")
    user["city"] = form.getfirst("city")
    user["state"] = form.getfirst("state")
    user["postcode"] = form.getfirst("postcode")

    # attempt to add the user to the database and check if it was successful
    if userhelper.addUser(user):
        userhelper.sendValidationEmail(user["username"], user["email"])
        notification = "Account created. A validation email has been sent to "+user["email"]+"."
    else:
        notification = "Account creation failed. Please try again."
elif "action" in form and "Login" in form.getlist("action"):
    # log me in
    if userhelper.loginUser(form.getfirst("username"), form.getfirst("password")):
        notification = "Successful! You have been logged in as "+form.getfirst("username")
        cookieSet = userhelper.createSessionCookie(form.getfirst("username"))
    else:
        notification = "Username or password incorrect. Please try again"
elif "action" in form and "Log out" in form.getlist("action"):
    # log me out
    if userhelper.isLoggedIn():
        userhelper.logOut(userhelper.getCurrentUser())

print http_header(cookieSet)


# 
# HTML STUFF
# 
if "search" in form:
    # If there's a search query, search for it
    # using code from pages.py
    string = pages.search("".join(form.getlist("search")), form.getfirst("category"))
elif "login" in form.getlist("page"):
    # if the login button was clicked
    # then load to the login page
    if userhelper.isLoggedIn():
        string = pages.accountDetail(userhelper.getCurrentUser())
    else:
        string = pages.login()
elif "validate" in form.getlist("page"):
    # if we need to validate a user's account
    # then we validate a user's account
    userHash = form.getfirst("user")
    validated = userhelper.validateUser(userHash)
    string = pages.validate(validated)
elif "book-detail" in form.getlist("page"):
    # if a book page is requested
    # get the page for that book
    string = pages.bookDetail(form.getfirst("book"))
elif "account-detail" in form.getlist("page"):
    # if the user page is requested
    # get the page for that user
    # as long as they're logged in
    if userhelper.loggedInAs(form.getfirst("username")):
        string = pages.accountDetail(form.getfirst("username"))
    else:
        string = pages.error()
else:
    # otherwise, home page
    string = pages.mekong(form, notification=notification)

print string