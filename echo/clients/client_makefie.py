import socket
import msg

def client(server_addr):
    """Client - converting to file-like object to allow buffered I/O

    Assumption: request/response messages ending with LF
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)       # connect to server process
    # Note: binary mode preserve the data
    #       does not convert encodings and line ending as in text mode.
    file = sock.makefile('rwb')     # file-like obj in read/write binary mode

    sent_bytes = []
    recv_bytes = []
    for message in msg.msgs(20, length=2000):
        n_sent = file.write(message)
        file.flush()     # flush-out buffer to send immediately
        sent_bytes.append(n_sent)
        data = file.readline()     # receive response
        if not data:
            break
        recv_bytes.append(len(data))
    file.close()
    sock.close()
    msg.report(sent_bytes, recv_bytes)

if __name__ == '__main__':
    client(('np.hufs.ac.kr', 7))
