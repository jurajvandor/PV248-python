import http.server
import sys


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content type", "text/json")
        self.end_headers()

    def do_POST(self):
        self.send_response(200)


port = int(sys.argv[1])

server = http.server.HTTPServer(("", port), MyHandler)
server.serve_forever()


