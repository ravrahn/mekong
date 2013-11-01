import bookhelper

def fancyDate(date):
    date = date.split("-")

    if len(date) != 3:
        return "Unknown date"

    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    newDate = "%s %s, %s" % (months[int(date[1])], date[2], date[0])

    return newDate

def getHeader(query="", category="all"):
    '''
    in future, will check if user is logged in, etc.
    '''
    username = "Login or Register"
    headerSrc = "header.html"

    # if user is logged in.
    # then use the logged-in header
    # comment in haiku

    headerFile = open(headerSrc, "r")
    header = headerFile.read()
    headerFile.close()

    return header % { "username": username, "query": query, "category": category }

def mekong(title, notification=""):
    mekongFile = open("mekong.html", "r")
    mekong = mekongFile.read()
    mekongFile.close()

    resultFile = open("result.html", "r")
    result = resultFile.read()
    resultFile.close()

    featuredArr = bookhelper.featuredBooks()
    featuredString = ""
    for book in featuredArr:
        featuredString += result % book 

    topArr = bookhelper.topBooks()
    topString = ""
    for book in topArr:
        topString += result % book

    notificationFile = open("notification.html", "r")
    if notification != "":
        notification = notificationFile.read() % notification
    notificationFile.close()

    return mekong % { "header":getHeader(), "featured": featuredString, "top-ten": topString, "notification": notification }

def login():
    # load the login html
    # and return it as a string
    loginFile = open("login.html", "r")
    login = loginFile.read()
    loginFile.close()

    return login % { "header":getHeader() }

def validate(validated):

    validate = ""
    if validated:
        validateFile = open("valid.html", "r")
        validate = validateFile.read()
        validateFile.close()
    else:
        validateFile = open("invalid.html", "r")
        validate = validateFile.read()
        validateFile.close()

    return validate % { "header": getHeader() }


def search(query, category):
    searchFile = open("search.html", "r")
    search = searchFile.read()
    searchFile.close()

    resultFile = open("result.html", "r")
    result = resultFile.read()
    resultFile.close()

    books = bookhelper.searchBooks(query, category)

    string = ""
    for book in books:
        string += result % book #{ "isbn": book.get("isbn"), "imgsrc": book.get("largeimageurl"), "title": book.get("title"), "author": book.get("authors"), "price": book.get("price"), "rank": book.get("salesrank") }

    return search % { "header":getHeader(query=query, category=category), "query": query, "numResults": str(len(books)) , "results": string }

def bookDetail(isbn):
    bookDetailFile = open("bookDetail.html", "r")
    bookDetail = bookDetailFile.read()
    bookDetailFile.close()

    book = bookhelper.getBook(isbn)

    book["header"] = getHeader()

    book["releasedate"] = fancyDate(book["releasedate"])

    return bookDetail % book
