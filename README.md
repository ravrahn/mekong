# COMP2041 13s2 Assignment 2 - Mekong
The code in this repo is live [here](http://owencassidy.me/apps/mekong/)

## My Solution

The CSS of the website, and of course the html, was written completely from scratch - no Bootstrap. It took longer but I think it's among the most unique (and hopefully good) looking solutions. It took some time but I think it paid off.

The 'backend' of the website is written entirely in Python, and data is stored in a couple of SQLite3 databases.

#### mekong.cgi
This is the main file. It's split into two main parts, both dealing with form data - the "action", and the "page".

An "action" is the result of (very nearly) any form submit button in the site. The first half of the file will carry out the action (if any) given to it - for example, creating a user, logging in or out, adding a book to the cart, or processing orders.

A "page" is in the query string - `?page=login`, for example, would load the login page. The second half of the file will print the appropriate page.

This file's main job is to call functions in other files based on the query string and form data. For that reason, it's fairly short and simple - and heavily commented.

The only other part of this file is the http header function, which is fairly self-explanitory - it prints the end of the http header, setting a cookie if necessary, but generally just sending the content type.

#### Modules

##### pages.py
To produce each page, I used a crude and unsophisticated templating method (We weren't allowed to use proper templating engines - only modules that were installed already on CSE machines). Each page was written in static html, with Python format strings (`%(word)s`) in place of dynamic content, or often-repeated content like the fixed header. Every page (and the header) has a function that generates it in `pages.py`, using any variables it needs (username, usually).

##### userhelper.py
This module contains lots of functions pertaining to users. It manages the creation of user accounts, validating users, sending emails to users, the users' carts, their orders, everything. It does a lot of interfacing with the `users.db` file, which contains all the user data in three tables - users, carts, and orders. The schema is available in the databasehelper module. This module has a lot of imports because of the variety of actions it is responsible for. It should probably be two or three modules, not one.

##### bookhelper.py
We were given a good deal of book data from Amazon in a file called `books.json`. JSON is fairly slow to query (because it's not made for storing data like this), so all the data has been moved to a SQLite3 database called books.db. This module interfaces with that database, for the most part. It contains functions for getting details about a specific book, searching the database for books (using the SQLite3 LIKE operator and some rather nice priority sorting), and the 'featured' (random) and 'top' (salesrank) books for the front page. It returns books as dictionaries containing all the necessary details, using a clever function that automatically turns SQLite3 query results into dictionaries. This plays well into my 'templating' system, because I can feed a book dictionary to the page and everything is taken care of automatically.

##### databasehelper.py

This was written in a hurry. It is three functions - one generates the books database from books.json, one generates an empty users database, the other runs them if they need to be run. It was made just in case either were ever made unavailable. In this file, the schema for the databases can be found.


## The Spec

####Introduction
Your goal in this assignment is to implement a simple but online shopping web site.

Most of you will have used online shopping sites and will have noticed at that are their core most sites have similar basic features:

Browse & search facilities to allow customers to find products.
A shopping cart where a customer accumulates products to be purchased.
Checkout where the customer supplies shipping and payment details.
Succesful shopping sites often have many other more sophisticated features such as personalisation and recommendations and for high volume on-line retailers like amazon.com, their site will be backed by a giant database server and hundreds of thousands of lines of server-side scripts. Your goal in this assignment is to look at some of the ideas behind e-commerce sites and see how they might be implemented in a simpler environment using Perl and text files.

You will do this by implementing mekong.com.au an online book store.

There is a model implementation which you can emulate. You do not have to match this model implementation precisely, you should generate different HTML, but you do have to provide the same basic functionality. You can provide extra/different functionality in a different manner but you can not take shortcut such as combining all functionality into a single screens.

There is a large amount of code you can use as a starting point.

This starting point code will be discussed in lectures & tutorials.

The assessment for this assignment (see below) will allow you to obtain a reasonable mark if you successfully complete some basic features. To assist you tackling the assignments requirements have been broken into several levels in approximate order of difficulty. You do not have to follow this implementation order but unless you are confident I'd recommend roughly following this order.

#####Check user's Passowrd (Level 0)

Change the login form to request a password & check this is correct.

#####Display Search results (Level 0)

The starting-point code you've been given displayu search results as simple text. They should be displayed in a HTML table complete with images.

#####Interface (Level 0)

Your web site must generate nicely formatted convenient-to-use web pages including appropriate navigation facilities and instructions for naive users. Although this is not a graphic design exercise you should produce pages with a common and somewhat distinctive look-and-feel. You may find CSS useful for this.
Note the model implementation does not meet this requirement and you do not have to match its poor layout & design.

#####Creating Accounts (Level 1)

Add a button & form to allow a user to create an account.

#####Basket (Level 1)

Add a button to display the user's basket.

#####Check Out (Level 1)

Add buttons and form to allow the user to checkout

#####Orders (Level 1)

Add a button to allow the user to view their orders.

#####Add/details in Search results(Level 2)

Add buttons to allow users to view the details of any book in their search results and to add any book to their basket.

#####Drop/details in Basket (Level 2)

Add buttons to allow users to view the details of any book in their basket and to drop (remove) any book to their basket.

#####E-mail confirmation (Level 3)

You should confirm the e-mail address supplied when creating an account is valid and owned by the user, by sending an e-mail to the address containing a link necessary to complete account creation.
The model implemetation does not implement this.

#####Lost Password (Level 3)

Users who have lost their password should be able to reset their password via an e-mailed link.
The model implementation does not implement this.

#####Order Multiple Books (Level 3)

The code you have been given handles users buying multiple copies of books poorly.
Change the code so they users can easily order any number of a book.

This should be displayed as counts (not repeated copies of the book) and the user should be be able to easily modify the count - e.g. go from ordering 50 copies to 200 copies easily.

The model implemetation does not implement this.

#####Other Features (Level 4)

There are many other possible features. It will be possible to obtain marks for implementing relevant non-trivial features not described above.

####Data Files

Your web site needs to store information about customers, books, and the groups of books that customers intend to buy and the ones they have actually bought.
The starting point code you have been given assumes that present in the current directory is a file containing information about books named books.json. The starting point code contains appropriate functions to read this books file into a hash and to search the hash for particular books. Your code should not need to access the books file directly.

The starting point code you have been given creates, read & write data files in three of directories described below. For levels 0-2 all the code you need to manipulates the data in these directories has been given to you.

#####users
There is a file for each customer account in this directory. The name of the file is the customer's login name. Lines in this file specify the user's password, name, street, city, state, postcode and email. Each file is created by the new_account command and not subsequently changed.

#####baskets
There is a file in this directory for each (non-empty) shopping basket. Each basket is represented as a single file with the same name as the user who owns it. A user has only one shopping basket. There is one line in this file for each book in the user's basket. Each line contains only the book's ISBN. This file is created by the add command. It is modified by the add and drop commands. It is removed by the drop and checkout command. It is not removed by the quit command - it persists until the user next logs in.

#####orders
A directory containing information about orders. It contains three different kinds of files.
There is file for each user who has made an order, containing a complete history of orders made by that user. It consists only of order numbers, one per line.

There is one file for each order. The first three lines of that file specify the time the order was made (as seconds since Jan 1 1970), the credit card number used for that order and its expiry date. These three lines are followed by one line for each book in the order. Each line contains only the isbn of the book.

There is a single file named NEXT\_ORDER\_NUMBER which contains the number which should be used for the next order. If this file does not exist the starting point creates it with appropriate contents by checking what orders already exist (if any).

You do not have to use the above format to store data but as you've been given code to perform the level 0-2 operations for this data format. I expect most students will do so and unless you are very confident it is recommended you do so. If you use another data format you should import the supplied books into this format and have it available for when you demo your web site so testing can be conducted using a familiar set of books.

####Assumptions/Clarifications

You may submit multiple CGI files but the primary file must be named mekong.cgi You may submit other files to be used by your CGI script(s). If you have need to submit many other files or directory hierarchy, submit them as a tar file named files.tar. You do not need to submit books.json or the default user, baskets & orders directories.

Your CGI script must run on CSE's system.

You may use any Perl/Python/... package which is installed on CSE's system. You may with appropriate attribution use existing Javascript libraries, CSS or HTML. You can not otherwise use code written by another person.

I expect almost all students will use Perl to complete this assignment but you are permitted to use Python. You are not permitted to use other languages, except you may use some Javascript. Again Andrew won't be able to offer any help. A high mark for the assignment can be obtained without Javascript but at least a little Javascript is commonly employed in this situation.

If you chose to use a database to store data, note it can be tricky getting full database systems such as mysql set up on CSE systems - and Andrew won't be able to offer any help. Sqlite is recommended because its embedded, and hence much simpler to setup.

You should avoid running external programs, for example via system, back quotes or open in Perl or via subprocess in Python, where an equivalent operation could be performed simply in Perl/Python. You may be penalized if you do so.

You are permitted to run an external program to send e-mail, although this is possible from Perl & Python.
