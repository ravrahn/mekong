def http_header():
	return """Content-Type: text/html\n"""

def html_list(items):
	string = "<ul>\n"
	for item in items:
		string += "<li>"+item+"</li>\n"
	string += "</ul>"
	return string