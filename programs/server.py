#!/usr/bin/env python
"""
A very simple server in python
used to control gpio pins on the beaglebone black.

The server listens for POST requests on port
6410. It has no security at all, which means
that it accepts post-data from everyone.

Send a GET request::
    curl http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

Usage:
    nohup python3 server.py &
"""

# TODO: Add basic security
# TODO: Use dictionary for gpio name : file

import http.server
import urllib

PORT = 6410
gpio_path = "/sys/class/gpio/"

# If the param name is in here then we handle the value.
authorized_gpio = ["gpio60"]

class Server(http.server.BaseHTTPRequestHandler):

    def prepare_response(self, code):
        """
            Prepares the response that will be send back to the requester,
            along with the code.
        """
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def handle_gpio(self, key, value):
        """
            Very basic gpio handling, converts the value into 
            an int and then it writes it to the file.
        """
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
        """
            Handles the post request.
            If error is True then the handling has failed or the request is 
            invalid
        """
        error = False
        try:
            # The length of the request, in bytes.
            length = int(self.headers['content-length'])
            # Dictionary containing keys and values from the request.
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
        # Write response to the client.
        self.wfile.write(response.encode())

if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, Server)
    print('Starting server')
    httpd.serve_forever()
