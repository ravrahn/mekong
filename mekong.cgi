#!/usr/bin/python2.7
from cgi_helper import *
from books_class import *
import pages
import json
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()

print http_header()

print pages.login()

# print pages.landing()


# print makeBooks(json.load(open("books.json", "r")))
# works!

# dictionry replace %s's inside the html file
# print html % {"title":form}