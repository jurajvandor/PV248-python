import http.server
import http.client
import sys
import json


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True



class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        client = http.client.HTTPConnection(str(sys.argv[2]), timeout=1)
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        client.request("GET", "/", None, headers)
        res = client.getresponse()
        self.send_response(200)
        json_dict = dict()
        json_dict["code"] = res.getcode()
        body = str(res.read())
        json_dict["headers"] = res.getheaders()
        if res.getheader("Content-type")[0:17] == "application/json" and is_json(body):
            json_dict["json"] = body
        else:
            json_dict["content"] = body
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(json_dict).encode("UTF8")))


    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        data = self.rfile.read(length)
        loaded_json = json.loads(data)
        client = http.client.HTTPConnection(loaded_json["url"], timeout=loaded_json["timeout"])
        body = loaded_json["content"] if loaded_json["type"] == "POST" else None
        client.request(loaded_json["type"], "/", body, loaded_json["headers"])
        res = client.getresponse()
        json_dict = dict()
        json_dict["code"] = res.getcode()
        body = str(res.read())
        json_dict["headers"] = res.getheaders()
        if res.getheader("Content-type")[0:17] == "application/json" and is_json(body):
            json_dict["json"] = body
        else:
            json_dict["content"] = body
        self.send_header("Content-Type", "application/json")
        self.wfile.write(bytes(json.dumps(json_dict).encode("UTF8")))
        self.send_response(200)
        self.end_headers()


port = int(sys.argv[1])

server = http.server.HTTPServer(("", port), MyHandler)
server.serve_forever()

