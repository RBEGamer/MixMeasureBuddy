"""
MicroPyServer is a simple HTTP server for MicroPython projects.

@see https://github.com/troublegum/micropyserver

The MIT License

Copyright (c) 2019 troublegum. https://github.com/troublegum/micropyserver
Copyright (c) 2024 Marcel Ochsendorf - modification of loop
.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import re
import socket
import sys
import io

import re

""" HTTP response codes """
HTTP_CODES = {
    100: 'Continue',
    101: 'Switching protocols',
    102: 'Processing',
    200: 'Ok',
    201: 'Created',
    202: 'Accepted',
    203: 'Non authoritative information',
    204: 'No content',
    205: 'Reset content',
    206: 'Partial content',
    207: 'Multi status',
    208: 'Already reported',
    226: 'Im used',
    300: 'Multiple choices',
    301: 'Moved permanently',
    302: 'Found',
    303: 'See other',
    304: 'Not modified',
    305: 'Use proxy',
    307: 'Temporary redirect',
    308: 'Permanent redirect',
    400: 'Bad request',
    401: 'Unauthorized',
    402: 'Payment required',
    403: 'Forbidden',
    404: 'Not found',
    405: 'Method not allowed',
    406: 'Not acceptable',
    407: 'Proxy authentication required',
    408: 'Request timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length required',
    412: 'Precondition failed',
    413: 'Request entity too large',
    414: 'Request uri too long',
    415: 'Unsupported media type',
    416: 'Request range not satisfiable',
    417: 'Expectation failed',
    418: 'I am a teapot',
    422: 'Unprocessable entity',
    423: 'Locked',
    424: 'Failed dependency',
    426: 'Upgrade required',
    428: 'Precondition required',
    429: 'Too many requests',
    431: 'Request header fields too large',
    500: 'Internal server error',
    501: 'Not implemented',
    502: 'Bad gateway',
    503: 'Service unavailable',
    504: 'Gateway timeout',
    505: 'Http version not supported',
    506: 'Variant also negotiates',
    507: 'Insufficient storage',
    508: 'Loop detected',
    510: 'Not extended',
    511: 'Network authentication required',
}


def send_response(server, response, http_code=200, content_type="text/html", extend_headers=None):
    """ send response """
    server.send("HTTP/1.0 " + str(http_code) + " " + HTTP_CODES.get(http_code) + "\r\n")
    server.send("Content type:" + content_type + "\r\n")
    if extend_headers is not None:
        for header in extend_headers:
            server.send(header + "\r\n")
    server.send("\r\n")
    server.send(response)


def get_request_method(request):
    """ return http request method """
    lines = request.split("\r\n")
    return re.search("^([A-Z]+)", lines[0]).group(1)


def get_request_query_string(request):
    """ return http request query string """
    lines = request.split("\r\n")
    match = re.search("\\?(.+)\\s", lines[0])
    if match is None:
        return ""
    else:
        return match.group(1)


def parse_query_string(query_string):
    """ return params from query string """
    if len(query_string) == 0:
        return {}
    query_params_string = query_string.split("&")
    query_params = {}
    for param_string in query_params_string:
        param = param_string.split("=")
        key = param[0]
        if len(param) == 1:
            value = ""
        else:
            value = param[1]
        query_params[key] = value
    return query_params


def get_request_query_params(request):
    """ return http request query params """
    query_string = get_request_query_string(request)
    return parse_query_string(query_string)


def get_request_post_params(request):
    """ return params from POST request """
    request_method = get_request_method(request)
    if request_method != "POST":
        return None
    match = re.search("\r\n\r\n(.+)", request)
    if match is None:
        return {}
    query_string = match.group(1)
    return parse_query_string(query_string)


def unquote(string):
    """ unquote string """
    if not string:
        return ""

    if isinstance(string, str):
        string = string.encode("utf-8")

    bits = string.split(b"%")
    if len(bits) == 1:
        return string.decode("utf-8")

    res = bytearray(bits[0])
    append = res.append
    extend = res.extend

    for item in bits[1:]:
        try:
            append(int(item[:2], 16))
            extend(item[2:])
        except KeyError:
            append(b"%")
            extend(item)

    return bytes(res).decode("utf-8")

class MicroPyServer(object):

    def __init__(self, host="0.0.0.0", port=80):
        """ Constructor """
        self._host = host
        self._port = port
        self._routes = []
        self._connect = None
        self._on_request_handler = None
        self._on_not_found_handler = None
        self._on_error_handler = None
        self._sock = None

    def start(self):
        """ Start server """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen(1)
        print("Server start")
        while True:
            if self._sock is None:
                break
            try:
                self._connect, address = self._sock.accept()
                request = self.get_request()
                if len(request) == 0:
                    self._connect.close()
                    continue
                if self._on_request_handler:
                    if not self._on_request_handler(request, address):
                        continue
                route = self.find_route(request)
                if route:
                    route["handler"](request)
                else:
                    self._route_not_found(request)
            except Exception as e:
                self._internal_error(e)
            finally:
                self._connect.close()


    def loop_init(self):
        """ Start server """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen(1)
    
    def loop(self):
        print("Server start")

        if self._sock is None:
            return
        try:
            self._connect, address = self._sock.accept()
            request = self.get_request()
            if len(request) == 0:
                self._connect.close()
                return
            if self._on_request_handler:
                if not self._on_request_handler(request, address):
                    return
            route = self.find_route(request)
            if route:
                route["handler"](request)
            else:
                self._route_not_found(request)
        except Exception as e:
            self._internal_error(e)
        finally:
            self._connect.close()

    
    def stop(self):
        """ Stop the server """
        self._connect.close()
        self._sock.close()
        self._sock = None
        print("Server stop")

    def add_route(self, path, handler, method="GET"):
        """ Add new route  """
        self._routes.append(
            {"path": path, "handler": handler, "method": method})

    def send(self, data):
        """ Send data to client """
        if self._connect is None:
            raise Exception("Can't send response, no connection instance")
        self._connect.sendall(data.encode())

    def find_route(self, request):
        """ Find route """
        lines = request.split("\r\n")
        method = re.search("^([A-Z]+)", lines[0]).group(1)
        path = re.search("^[A-Z]+\\s+(/[-a-zA-Z0-9_.]*)", lines[0]).group(1)
        for route in self._routes:
            if method != route["method"]:
                continue
            if path == route["path"]:
                return route
            else:
                match = re.search("^" + route["path"] + "$", path)
                if match:
                    print(method, path, route["path"])
                    return route

    def get_request(self, buffer_length=4096):
        """ Return request body """
        return str(self._connect.recv(buffer_length), "utf8")

    def on_request(self, handler):
        """ Set request handler """
        self._on_request_handler = handler

    def on_not_found(self, handler):
        """ Set not found handler """
        self._on_not_found_handler = handler

    def on_error(self, handler):
        """ Set error handler """
        self._on_error_handler = handler

    def _route_not_found(self, request):
        """ Route not found handler """
        if self._on_not_found_handler:
            self._on_not_found_handler(request)
        else:
            """ Default not found handler """
            self.send("HTTP/1.0 404 Not Found\r\n")
            self.send("Content-Type: text/plain\r\n\r\n")
            self.send("Not found")

    def _internal_error(self, error):
        """ Internal error handler """
        if self._on_error_handler:
            self._on_error_handler(error)
        else:
            """ Default internal error handler """
            if "print_exception" in dir(sys):
                output = io.StringIO()
                sys.print_exception(error, output)
                str_error = output.getvalue()
                output.close()
            else:
                str_error = str(error)
            self.send("HTTP/1.0 500 Internal Server Error\r\n")
            self.send("Content-Type: text/plain\r\n\r\n")
            self.send("Error: " + str_error)
            print(str_error)

