import socket
import msg

def client(server_addr):
    """Client - read more date after shut-down
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)       # connect to server process

    sent_bytes = []
    recv_bytes = []
    for message in msg.msgs(20, length=2000):  # generate 20 msgs
        n_sent = sock.send(message)          # send message to server
        sent_bytes.append(n_sent)
        data = sock.recv(2048)      # receive response from server
        if not data:                # check if server terminates abnormally
            print('Server abnormally terminated')
            break
        recv_bytes.append(len(data))
    else:
        # Now all the messages sent. Terminate outgoing TCP connection.
        sock.shutdown(socket.SHUT_WR) # send eof mark (FIN)
        # Receive more for the remaining messages
        while True:
            data = sock.recv(2048)
            if not data:
                break
            recv_bytes.append(len(data))
    sock.close()
    msg.report(sent_bytes, recv_bytes)

if __name__ == '__main__':
    client(('np.hufs.ac.kr', 7))
