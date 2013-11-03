#!/usr/bin/python2.7
import os,sys,re,cgi,cgitb
import userhelper
import pages
import Cookie

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
    if userhelper.isCorrectPassword(form.getfirst("username"), form.getfirst("password")):
        cookieSet = userhelper.createSessionCookie(form.getfirst("username"))
        print http_header(cookieSet)
        print pages.redirect("http://cgi.cse.unsw.edu.au/~obca109/mekong/mekong.cgi")
        sys.exit()
    else:
        notification = "Username or password incorrect. Please try again"
elif "action" in form and "Log Out" in form.getlist("action"):
    # log me out
    if userhelper.isLoggedIn():
        userhelper.logOut(userhelper.getCurrentUser())
        cookieSet = Cookie.SimpleCookie()
        cookieSet["sessionid"] = ""
        cookieSet["sessionid"]["expires"] = "Thu, 01-Jan-1970 00:00:10 GMT"
elif "action" in form and "Add to Cart" in form.getlist("action"):
    # add the book to the cart
    book = form.getfirst("book")
    quantity = int(form.getfirst("quantity"))
    userhelper.addToCart(userhelper.getCurrentUser(), book, quantity)
elif "action" in form and "Update" in form.getlist("action"):
    # update the quantity
    book = form.getfirst("book")
    newQuantity = form.getfirst("quantity")
    username = form.getfirst("username")
    userhelper.setQuantity(username, book, newQuantity)
elif "action" in form and "Remove" in form.getlist("action"):
    # remove from cart
    book = form.getfirst("book")
    username = form.getfirst("username")
    userhelper.removeFromCart(username, book)
elif "action" in form and "Cancel" in form.getlist("action"):
    # remove from cart
    book = form.getfirst("book")
    username = form.getfirst("username")
    userhelper.removeFromOrders(username, book)
elif "action" in form and "Checkout" in form.getlist("action"):
    # checkout the books
    username = form.getfirst("username")
    creditCard = form.getfirst("credit-card")
    userhelper.checkout(username, creditCard)

print http_header(cookieSet)

# 
# HTML STUFF
# 
if "search" in form and "search" in form.getlist("page"):
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
elif "book-detail" in form.getlist("page") and "book" in form:
    # if a book page is requested
    # get the page for that book
    string = pages.bookDetail(form.getfirst("book"))
elif "account-detail" in form.getlist("page") and "username" in form:
    # if the user page is requested
    # get the page for that user
    string = pages.accountDetail(form.getfirst("username"))
elif "checkout" in form.getlist("page") and "username" in form:
    # if the checkout page is requested
    # and a user is provided
    string = pages.checkout(form.getfirst("username"))
elif "page" in form:
    string = pages.error()
else:
    # otherwise, home page
    string = pages.mekong(form, notification=notification)

print string