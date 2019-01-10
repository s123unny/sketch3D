from http.server import *
import socketserver
import json
import numpy as np
import geometric as geo
import rittai

#init content
contentDic = {}
content = ["index.html", "UI.css", "overlay.css", "webgl-utils.js", "glMatrix-0.9.5.min.js", "draw.js", "Kangaroo.json"]
for idx, element in enumerate(content):
	fp = open(element, "r")
	contentDic[element] = fp.read()
	fp.close()

def default(o):
	if isinstance(o, np.float64): 
		return float(o) 
	elif isinstance(o, np.int64):
		return int(o)

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
		if polygon.po2tri() == True:
			polygon.plot_show() #plot the polygon 
			threed = rittai.rt(polygon) 
			threed.run()
			Len = len(threed.vertex.reshape(1,-1)[0])
			res = {"vertexPositions":list(threed.vertex.reshape(1,-1)[0]), "vertexNormals": list(threed.norm.reshape(1,-1)[0]), "indices": list(threed.face.reshape(1,-1)[0]), "vertexFrontcolors": list([2 for i in range(Len)]), "vertexBackcolors": list([0.7392156862745098 for i in range(Len)])}
			res = json.dumps(res, default=default)
			self._set_headers()
			self.wfile.write(res.encode("utf-8"))
		else:
			self.send_response(404)
			self.end_headers()

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