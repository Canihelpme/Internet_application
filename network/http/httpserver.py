import socketserver
import time         # to know current time
import mimetypes    # to map filenames to MIME types
import headers      # your module 'headers.py'

class HTTPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print(self.request)
        # read request message
        method, path, protocol = self.rfile.readline().decode().split()
        req_headers = headers.parse_headers(self.rfile)
        content_length = req_headers.get('Content-length')
        if content_length:      # if request body exists
            body = self.rfile.read(int(content_length))
        else:
            body = None
        print(method, path, protocol)
        print(req_headers)
        if content_length:
            print(body)

        # read content from file name: '.' + path
        file = '.' + path
        try:
            f = open(file, 'rb')
        except Exception as e:
            content = None
        else:
            content = f.read()
            f.close()
        # Build response message
        if content:
            print('HTTP/1.1 200 OK')
            self.wfile.write(b'HTTP/1.1 200 OK\r\n')
        else:
            print('HTTP/1.1 404 Not found')
            self.wfile.write(b'HTTP/1.1 404 not found\r\n')
        res_headers = {}
        res_headers['Date'] = time.asctime()
        res_headers['Server'] = 'MyServer/1.0'
        res_headers['Connection'] = 'close' if req_headers.get('Connection') == 'close' else 'keep-alive'
        if content:
            content_type, encoding = mimetypes.guess_type(file)
            res_headers['Accept-Ranges'] = 'bytes'
            res_headers['Content-type'] = content_type
            res_headers['Content-length'] = str(len(content))
        print(res_headers)
        self.wfile.write(headers.to_bytes(res_headers))
        if content:
            self.wfile.write(content)
        self.wfile.flush()

with socketserver.TCPServer(('', 8080), HTTPHandler) as http_server:
    # http_server.timeout = 5
    http_server.serve_forever()
