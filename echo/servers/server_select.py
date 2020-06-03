from socket import socket, AF_INET, SOCK_STREAM
import selectors

sel = selectors.DefaultSelector()

# call-back functions
def accept(sock, mask):
    conn, client_address = sock.accept()
    conn.setblocking(False) # non-blocking socket
    sel.register(conn, selectors.EVENT_READ, echo)
    print('Connection from', client_address)

def echo(conn, mask):
    data = conn.recv(1024)  # Should be ready
    if data:
        conn.sendall(data)  # Hope it won't block
    else:
        client_address = conn.getpeername()
        sel.unregister(conn)
        conn.close()
        print('Client closed {}'.format(client_address))

def echo_server(my_port):
    """Echo Server - I/O multiplexing"""

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setblocking(False)
    sock.bind(('', my_port))
    sock.listen(5)
    sel.register(sock, selectors.EVENT_READ, accept)
    print('Server started')

    while True:
        events = sel.select(timeout=1)
        print(events)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    echo_server(10007)