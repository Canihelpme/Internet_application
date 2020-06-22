import socket
import msg

def client(server_addr):
    """Client - converting to file-like object to allow buffered I/O

    Assumption: request/response messages ending with LF
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)       # connect to server process
    # file-like obj in read/write binary mode  
    # Note: binary mode preserve the data (not convert encodings and line ending)
   
    rfile = sock.makefile('rb')    # incoming stream
    wfile = sock.makefile('wb')   # outgoing stream
    sent_bytes = []
    recv_bytes = []
    for message in msg.msgs(20, length=2000):
        n_sent = wfile.write(message)
        wfile.flush()     # flush-out user buffer to send immediately
        sent_bytes.append(n_sent)
        data = rfile.readline()     # incoming line message
        if not data:                 # check if server terminates abnormally
            print('Server abnormally terminated')
            break
        recv_bytes.append(len(data))
    sock.close()
    msg.report(sent_bytes, recv_bytes)

if __name__ == '__main__':
    client(('np.hufs.ac.kr', 7))
