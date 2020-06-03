
"""
보낸 만큼 서버가 받는 것은 아니다!!
"""

import socket
import msg

def client(server_addr):
    """Incorrect client
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)       # connect to server process

    sent_bytes = []
    recv_bytes = []
    for message in msg.msgs(20, length=2000):  # generate 20 msgs
        n_sent = sock.send(message) # send message to server
        sent_bytes.append(n_sent)
        data = sock.recv(2048)      # receive response from server
        recv_bytes.append(len(data))
    sock.close()                    # send eof mark (FIN)

    msg.report(sent_bytes, recv_bytes)

if __name__ == '__main__':
    client(('np.hufs.ac.kr', 7))

