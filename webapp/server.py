#!/usr/bin/env python3

from pathlib import Path
import mimetypes
import urllib.parse
from http.server import BaseHTTPRequestHandler
from routes.main import routes
from handler.handlers import handle_post, handle_get_data


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_string = post_data.decode('utf-8')
        post_params = urllib.parse.parse_qs(post_string)

        print(f"POST in {self.path}")
        print(f"POST data: {post_params}")

        self.respond(post_params)
   
    def handle_http(self, post_data=None):
        status = 200
        content_type = "text/plain"
        response_content = ""

        if self.path in routes:
            if post_data is not None:
                print(f"Handle post for {self.path}")
                handle_post(self.path, post_data)
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return b""
            elif self.path == "/data":
                content_type = "application/json"
                response_content = handle_get_data()
            elif 'template' in routes[self.path]:
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
                response_content = "Method not allowed"
                status = 405
        else:
            content_type = "text/plain"
            response_content = "404 Not Found"

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(response_content, "UTF-8")

    def respond(self, post_data=None):
        content = self.handle_http(post_data)
        self.wfile.write(content)

