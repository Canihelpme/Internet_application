import socket
import threading, logging, selectors

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
# default log level
# logging.basicConfig(format=logging.WARNING'%(threadName)s: %(message)s')

class RequestHandler:
    def __init__(self, request, client_address, server):
        threading.Thread.__init__(self)
        self.request = request
        self.cli_addr = client_address
        self.server = server    # server object
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        self.rfile = self.request.makefile('rb')
        self.wfile = self.request.makefile('wb')

    def handle(self):
        pass

    def finish(self):
        if not self.wfile.closed:
            self.wfile.flush()
        self.wfile.close()
        self.rfile.close()


class EchoRequestHandler(RequestHandler):
    def handle(self):
        while True:
            line = self.rfile.readline()
            if not line:       # eof when the socket closed
                logging.info('Client closing: {}'.format(self.cli_addr))
                break
            logging.debug('Rcvd from {}: {} bytes'.format(self.cli_addr, len(line)))
            self.wfile.write(line)         # send a reply to the client
            self.wfile.flush()      # flush out the buffer. Send immediately


class ThreadingTCPServer:
    def __init__(self, server_address, HandlerClass):
        # make listening socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse port number if used
        sock.bind(server_address)
        sock.listen(5)
        self.sock = sock
        self.HandlerClass = HandlerClass
        # to allow non-blocking accept for listening socket
        self.sock.setblocking(False)  # set non-blocking mode
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.sock, selectors.EVENT_READ)

    def serve_forever(self):
        logging.info('Server started')
        try:
            while True:                     # do forever (until process killed)
                ready = self.sel.select(timeout=0.5)    # poll evert 0.5 sec even though not ready
                if ready:        # if listening socket readable
                    try:
                        request, client_address = self.sock.accept()
                    except OSError as e:
                        logging.exception('Ignore socket error in accept: {}'.format(e))
                        continue
                    logging.info('Connection from {}'.format(client_address))
                    t = threading.Thread(target=self.process_request,
                                         args=(request, client_address))
                    t.setDaemon(True)  # as daemon thread
                    t.start()
                else:           # timeout
                    pass
        except Exception as e:
            logging.exception('Exception at listening:'.format(e))
            raise               # abort server
        finally:
            self.sock.close()

    def process_request(self, request, client_address):
        """Invoke the handler to process the request"""
        try:
            handler = self.HandlerClass(request, client_address, self)
        except Exception as e:
            logging.exception('Exception in processing request from {}: {}'.
                              format(client_address, e))
        finally:
            request.close()

if __name__ == '__main__':
    server = ThreadingTCPServer(('', 10007), EchoRequestHandler)
    server.serve_forever()

