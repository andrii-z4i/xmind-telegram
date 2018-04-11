from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from socketserver import ThreadingMixIn
import typing
from urllib.parse import urlparse, parse_qs
import json


class Response(object):
    def __init__(self, response_code: int, body) -> None:
        self.code = response_code
        _body = body if type(body) is str else json.dumps(body)
        self.body = _body.encode()

class Request(object):
    def __init__(self, command, scheme, address, path, query, body, headers):
        self.command = command
        self.scheme = scheme
        self.address = address
        self.path = path
        self.query = query
        self.body = body
        self.headers = headers


class ResponseQueue(object):
    def __init__(self):
        super(ResponseQueue, self).__init__()
        self.response: typing.List[Resposne] = []

    def add_response(self, next_response: Response) -> None:
        self.response.append(next_response)

    def get_next_response(self) -> Response:
        return self.response.pop(0)


class QueryHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)
        self.server.last_request = Request(self.command, self.server.scheme,
                                    self.server.listen_address, url.path, query, body, self.headers)
        self.server.requests.append(self.server.last_request)
        next_response: Response = self.server.responses.get_next_response()
        self.send_response(next_response.code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(next_response.body)


class SimpleServer(ThreadingMixIn, HTTPServer, Thread):
    def __init__(self, listen_addr, query_handler=QueryHandler):
        self.listen_address = listen_addr
        self.scheme = 'http'
        self.requests: typing.List[Request] = []
        self.responses: ResponseQueue = ResponseQueue()

        HTTPServer.__init__(self, listen_addr, query_handler)
        self.__listen_addr = self.socket.getsockname()
        Thread.__init__(self)

    def listen_addr(self):
        return self.__listen_addr

    def run(self):
        self.serve_forever()

    def stop(self):
        self.shutdown()
        self.server_close()
