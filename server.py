from http.server import *
import socketserver
import json
import numpy as np
import geometric as geo

#init content
contentDic = {}
content = ["index.html", "UI.css", "overlay.css", "webgl-utils.js", "glMatrix-0.9.5.min.js", "draw.js", "Kangaroo.json"]
for idx, element in enumerate(content):
	fp = open(element, "r")
	contentDic[element] = fp.read()
	fp.close()

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		pathtype = self.path.split(".")[-1]
		if pathtype == "css":
			self.send_header('Content-type', 'text/css')
		elif pathtype == "js":
			self.send_header('Content-type', 'text/javascript')
		elif pathtype == "json":
			self.send_header('Content-type', 'application/json')
		else:
			self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		if self.path == "/":
			self.wfile.write(contentDic["index.html"].encode("utf-8"))
		else:
			self.wfile.write(contentDic[self.path[1:]].encode("utf-8"))

	def do_HEAD(self):
		self._set_headers()
		
	def do_POST(self):
		print ("post")
		length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(length).decode('utf-8')
		data = json.loads(post_data)
		polygon = geo.geometric(data)
		polygon.po2tri()
		polygon.plot_show() #plot the polygon 
		self._set_headers()
		self.wfile.write("<html><body><h1>POST!</h1></body></html>".encode("utf-8"))

def run(server_class=HTTPServer, handler_class=S, port=8000):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	httpd.serve_forever()


if __name__ == "__main__":
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()