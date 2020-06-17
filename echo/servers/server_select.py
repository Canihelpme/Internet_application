"""
Echo Server - I/O multiplexing version
    works well either of blocking or non-blocking sockets
"""

from socket import socket, AF_INET, SOCK_STREAM, SHUT_WR
import selectors
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
sel = selectors.DefaultSelector()

# call-back when listening socket is ready
def accept(sock, mask):
    conn, client_address = sock.accept()
    conn.setblocking(False) # non-blocking socket
    sel.register(conn, selectors.EVENT_READ, data=echo)
    logging.info(f'Client enters: {client_address}')

# call-back when connected socket is ready
def echo(conn, mask):
    data = conn.recv(1024)  # Should be ready
    if data:
        conn.sendall(data)  # Hope it won't block
        logging.debug(f'echo({conn.fileno()}) {len(data)} bytes')
    else:
        logging.info(f'Client closing: {conn.getpeername()}')
        shut_down(conn)

def shut_down(conn):
    try:
        sel.unregister(conn)
        conn.close()
    except Exception as e:      # already closed socket for instance
        logging.error(e)

def echo_server(my_port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setblocking(False)
    sock.bind(('', my_port))
    sock.listen(5)
    sel.register(sock, selectors.EVENT_READ, data=accept)  # connection completion event
    logging.info(f'Server listens: {sock.getsockname()}')
    
    while True:
        events = sel.select(timeout=0.5)
        for key, mask in events:
            callback = key.data
            try:
                callback(key.fileobj, mask)
            except OSError as e:        # socket.error handling
                logging.error(f'Error in {callback.__name__} callback: {e}')
                shut_down(key.fileobj)
                if key.fileobj is sock: # terminate in case of the listening socket error
                    import sys
                    sys.exit(1)
                # continue when error occurs out of the connected sockets


if __name__ == '__main__':
    echo_server(10007)