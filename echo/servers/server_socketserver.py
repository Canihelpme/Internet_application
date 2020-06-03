import socketserver

class EchoRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            line = self.rfile.readline()
            if not line:       # eof when the socket closed
                break
            self.wfile.write(line)         # send a reply to the client
            self.wfile.flush()      # flush out the buffer. Send immediately


server = socketserver.ThreadingTCPServer(('', 10007), EchoRequestHandler)
server.serve_forever()