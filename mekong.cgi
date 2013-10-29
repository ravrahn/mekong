#!/usr/bin/python2.7
import os,re,cgi,cgitb
from books_helper import *
import pages

cgitb.enable()

form = cgi.FieldStorage()

def http_header():
    return """Content-Type: text/html\n"""

print http_header()

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
    string = pages.mekong(form)

print string