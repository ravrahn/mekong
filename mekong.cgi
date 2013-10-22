#!/usr/bin/python2.7
from cgi_helper import *
from books_class import *
import pages
import json
import os
import re
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()

print http_header()

# if "Login" in form.getlist("action"):
# 	if os.path.exists(form.getlist("username")):
# 		userFile = open(form.getlist("username"), "r")
# 		password = userFile.readlines()[0]
# 		re.sub(r"password=([A-Za-z0-9]+)", r"\1", password)
# 		if form.getlist("password") == password:
# 			# log them in
# elif "Create Account" in form.getlist("action"):
# 	if not os.path.exists(form.getlist("username")):
# 		userFile = open(form.getlist("username"), "w")
# 		userFile.write("password="+form.getlist("password")+"\n")
# 		user


if "login" in form.getlist("page"):
	string = pages.login()
else:
	string = pages.mekong(form)

print string