#!/usr/bin/env python3

from pathlib import Path
import mimetypes
from http.server import BaseHTTPRequestHandler
from routes.main import routes


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond()

    def do_POST(self):
        return
   
    def handle_http(self):
        status = 200
        content_type = "text/plain"
        response_content = ""

        if self.path in routes:
            print(routes[self.path])
            route_content = routes[self.path]['template']
            filepath = Path(route_content)
            print("Requested file: {}".format(filepath))
            if filepath.is_file():
                content_type, _ = mimetypes.guess_type(str(filepath))
                if content_type is None:
                    content_type = "application/octet-stream"
                response_content = open(route_content)
                response_content = response_content.read()
            else:
                content_type = "text/plain"
                response_content = "404 Not Found"
        else:
            content_type = "text/plain"
            response_content = "404 Not Found"

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(response_content, "UTF-8")

    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)
