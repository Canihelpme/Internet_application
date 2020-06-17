'''
Threading TCP server with request handlers
'''
import socket
import threading, logging, selectors

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
# default log level
# logging.basicConfig(level=logging.WARNING, format='%(threadName)s: %(message)s')

class BaseRequestHandler:
    def __init__(self, request, client_address, server):
        self.request = request
        self.cli_addr = client_address
        self.server = server    # can access server attributes
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        pass

    def finish(self):
        pass

class StreamRequestHandler(BaseRequestHandler):
    def setup(self):
        self.rfile = self.request.makefile('rb')
        self.wfile = self.request.makefile('wb', buffering=0) # no buffering

    def finish(self):
        if not self.wfile.closed:
            self.wfile.flush()
        self.wfile.close()
        self.rfile.close()


class ThreadingTCPServer:
    def __init__(self, server_address, HandlerClass):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse port number if used
        sock.bind(server_address)
        sock.listen(5)
        self.sock = sock
        self.HandlerClass = HandlerClass

    def serve_forever(self):
        logging.info(f'Server started: {self.sock.getsockname()}')
        try:
            while True:                     # do forever (until process killed)
                request, client_address = self.sock.accept()
                logging.info(f'Connection from {client_address}')
                t = threading.Thread(target=self.process_request,
                                        args=(request, client_address))
                t.setDaemon(True)  # as daemon thread
                t.start()
        except:
            self.server_close()
            raise

    def process_request(self, request, client_address):
        """Invoke the handler to process the request"""
        try:
            handler = self.HandlerClass(request, client_address, self)
        except Exception as e:
            logging.exception(f'Exception in processing request from {client_address}: {e}')
        finally:
            request.close()

    def server_close(self):
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.server_close()


if __name__ == '__main__':
    # Echo server implemented by extending request handler
    class EchoRequestHandler(StreamRequestHandler):
        def handle(self):
            while True:
                line = self.rfile.readline()
                if not line:
                    break
                logging.debug(f'Rcvd from {self.cli_addr}: {len(line)} bytes')
                self.wfile.write(line)         # send a reply to the client
            logging.info(f'Client {self.cli_addr} closing')


    # server = ThreadingTCPServer(('', 10007), EchoRequestHandler)
    # server.serve_forever()
    with ThreadingTCPServer(('', 10007), EchoRequestHandler) as server:
        server.serve_forever()

