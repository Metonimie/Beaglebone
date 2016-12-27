#!/usr/bin/env python
"""
A very simple server in python
used to control gpio pins on the beaglebone black.

Send a GET request::
    curl http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

Usage:
    nohup python3 server.py &
"""

import http.server
import urllib
import cgi

PORT = 6410
gpio_path = "/sys/class/gpio/"
authorized_gpio = ["gpio60"]

class Server(http.server.BaseHTTPRequestHandler):

    def prepare_response(self, code):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def handle_gpio(self, key, value):
        try:
            clean_value = int(value)
            with open("{}{}/value".format(gpio_path, key), mode="w") as file:
                file.write(str(clean_value))
                return False
        except ValueError as e:
            print(e)
        except Exception as e:
            print("Exception: {}".format(e))
        return True

    def unsupported(self):
        self.wfile.write("Go Away!\n".encode())

    def do_GET(self):
        self.unsupported()

    def do_HEAD(self):
        self.unsupported()

    def do_POST(self):
        error = False
        try:
            length = int(self.headers['content-length'])
            postvars = urllib.parse.parse_qs(self.rfile.read(length))
            for key, value in postvars.items():
                clean_key = key.decode()
                clean_value = value[0].decode()
                print("Received: " + clean_key + " : " + clean_value)
                if clean_key in authorized_gpio:
                    error = self.handle_gpio(clean_key, clean_value)
                else:
                    error = True
        except Exception as e:
            print(e)
            error = True

        response = None
        if not error:
            self.prepare_response(200)
            response = "Operation authorized.\n"
        else:
            self.prepare_response(403)
            response = "Go away!\n"
        self.wfile.write(response.encode())

if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, Server)
    print('Starting httpd...')
    httpd.serve_forever()

