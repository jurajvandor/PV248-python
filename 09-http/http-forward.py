import http.server
import http.client
import sys
import json
import socket


def is_json(maybe_json):
    try:
        json.loads(maybe_json)
    except ValueError:
        return False
    return True


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        client = http.client.HTTPConnection(str(sys.argv[2]), timeout=1)
        headers = self.headers
        try:
            client.request("GET", "", None, headers)
        except socket.timeout:
            self.send_json({"code": "timeout"})
        else:
            self.create_json(client.getresponse())

    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        data = self.rfile.read(length)
        try:
            loaded_json = json.loads(data)
        except ValueError:
            self.send_json({"code": "invalid json"})
            return
        if "url" not in loaded_json.keys() or ("type" in loaded_json.keys() and "content" not in loaded_json.keys() and loaded_json["type"] == "POST"):
            self.send_json({"code": "invalid json"})
            return
        timeout = loaded_json["timeout"] if "timeout" in loaded_json.keys() else 1
        body = loaded_json["content"] if "type" in loaded_json.keys() and loaded_json["type"] == "POST" else None
        headers = loaded_json["headers"] if "headers" in loaded_json.keys() else dict()
        client = http.client.HTTPConnection(loaded_json["url"], timeout=timeout)
        try:
            client.request(loaded_json["type"], "", body, headers)
        except socket.timeout:
            self.send_json({"code": "timeout"})
        else:
            self.create_json(client.getresponse())

    def create_json(self, response):
        self.send_response(200)
        json_dict = dict()
        json_dict["code"] = response.getcode()
        body = str(response.read())
        json_dict["headers"] = response.getheaders()
        if response.getheader("Content-Type")[0:16] == "application/json" and is_json(body):
            json_dict["json"] = json.loads(body)
        else:
            json_dict["content"] = body
        self.send_json(json_dict)

    def send_json(self, json_dict):
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(json_dict).encode()))


port = int(sys.argv[1])

server = http.server.HTTPServer(("", port), MyHandler)
server.serve_forever()

