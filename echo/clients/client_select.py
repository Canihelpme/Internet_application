import socket
import msg
import selectors


def client(server_addr):
    """Client - read more date after shut-down
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)       # connect to server process
    sock.setblocking(False)         # non-blocking socket

    sel = selectors.DefaultSelector()
    sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE)
    it = iter(msg.msgs(100, length=2000))  # convert as iterable
    sent_bytes = []
    recv_bytes = []
    keep_running = True

    while keep_running:
        events = sel.select(timeout=1)

        for key, mask in events:
            conn = key.fileobj

            # recv if socket becomes readable
            if mask & selectors.EVENT_READ:
                print('readable')
                data = conn.recv(2048)
                if not data:
                    print('Server closing')
                    sel.unregister(conn)
                    keep_running = False
                    break
                recv_bytes.append(len(data))

            # sendall if socket becomes writable
            if mask & selectors.EVENT_WRITE:
                print('writable')
                try:
                    message = next(it)
                except StopIteration:  # no more messages
                    # Do not check writable.
                    sel.modify(conn, selectors.EVENT_READ)
                    conn.shutdown(socket.SHUT_WR)
                    break
                conn.sendall(message)
                sent_bytes.append(len(message))

            # if mask & (selectors.EVENT_WRITE | selectors.EVENT_READ):
            #     print('timeout')

        # end for
    # end while

    sock.close()
    msg.report(sent_bytes, recv_bytes)

if __name__ == '__main__':
    client(('np.hufs.ac.kr', 7))
