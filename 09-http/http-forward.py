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


def url_parse(url):
    if "/" not in url:
        return url, ""
    if "//" in url:
        split = url.split("/", 3)
        return split[2], "/" + split[3]
    else:
        split = url.split("/", 1)
        return split[0], "/" + split[1]


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = url_parse(str(sys.argv[2]))
        client = http.client.HTTPConnection(parsed_url[0], timeout=1)
        headers = self.headers
        try:
            client.request("GET", parsed_url[1], None, headers)
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
        parsed_url = url_parse(loaded_json["url"])
        client = http.client.HTTPConnection(parsed_url[0], timeout=timeout)
        try:
            client.request(loaded_json["type"], parsed_url[1], body, headers)
        except socket.timeout:
            self.send_json({"code": "timeout"})
        else:
            self.create_json(client.getresponse())

    def create_json(self, response):
        json_dict = dict()
        json_dict["code"] = response.getcode()
        json_dict["headers"] = response.getheaders()
        body = response.read()
        try:
            decoded = is_json(body.decode())
        except UnicodeDecodeError:
            json_dict["content"] = str(body)
        else:
            if decoded:
                json_dict["json"] = json.loads(body.decode())
            else:
                json_dict["content"] = str(body.decode())
        self.send_json(json_dict)

    def send_json(self, json_dict):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(json_dict).encode()))


port = int(sys.argv[1])

server = http.server.HTTPServer(("", port), MyHandler)
server.serve_forever()

