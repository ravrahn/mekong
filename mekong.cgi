#!/usr/bin/python2.7
import os,re,cgi,cgitb
import userhelper
import pages

cgitb.enable()

form = cgi.FieldStorage()

print """Content-Type: text/html\n
"""

notification = ""

if "action" in form and "Create Account" in form.getlist("action"):
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

    if userhelper.addUser(user):
        # userhelper.sendVerificationEmail(username)
        notification = "Account created. A verification email has been sent to "+user["email"]+"."
    else:
        notification = "Account creation failed. Please try again."

if "search" in form:
    # If there's a search query, search for it
    # using code from pages.py
    string = pages.search("".join(form.getlist("search")), form.getfirst("category"))
elif "login" in form.getlist("page"):
    # if the login button was clicked
    # then load to the login page
    string = pages.login()
elif "book-detail" in form.getlist("page"):
    # if a book page is requested
    # get the page for that book
    string = pages.bookDetail(form.getfirst("book"))
elif "account-detail" in form.getlist("page"):
    # if the user page is requested
    # get the page for that user
    # as long as they're logged in
    if True: #loggedInAs(form.getlist("userid")):
        string = pages.accountDetail(form.getfirst("userid"))
    else:
        string = pages.error()
else:
    # otherwise, home page
    string = pages.mekong(form, notification=notification)

print string