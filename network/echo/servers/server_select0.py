"""
Echo Server - I/O multiplexing version without logging and exception handling
    works well either of blocking or non-blocking sockets
"""

from socket import socket, AF_INET, SOCK_STREAM
import selectors

sel = selectors.DefaultSelector()

# call-back when listening socket is ready
def accept(sock, mask):
    conn, client_address = sock.accept()
    conn.setblocking(False) # non-blocking socket
    sel.register(conn, selectors.EVENT_READ, data=echo)
    print(f'Client enters: {client_address}')

# call-back when connected socket is ready
def echo(conn, mask):
    data = conn.recv(1024)  # Should be ready
    if data:
        conn.sendall(data)  # Hope it won't block
        print(f'echo({conn.fileno()}) {len(data)} bytes')
    else:
        print(f'Client closing: {conn.getpeername()}')
        sel.unregister(conn)
        conn.close()

def echo_server(my_port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setblocking(False)
    sock.bind(('', my_port))
    sock.listen(5)
    sel.register(sock, selectors.EVENT_READ, data=accept)  # connection completion event
    print(f'Server listens: {sock.getsockname()}')
    
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    echo_server(10007)