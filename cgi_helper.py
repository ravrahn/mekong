def http_header():
	return """Content-Type: text/html\n"""

def html_header(title="mekong"):
	return """<!DOCTYPE html>
<html lang="en">
<head>
	<title>"""+title+"""</title>
	<link rel="stylesheet" type="text/css" href="mekong.css">
</head>
<body>"""

def html_footer():
	return """</body>
</html>"""

def html_title(name, size=1):
	return "<h"+str(size)+">"+name+"</h"+str(size)+">"

def html_list(items):
	string = "<ul>\n"
	for item in items:
		string += "<li>"+item+"</li>\n"
	string += "</ul>"
	return string