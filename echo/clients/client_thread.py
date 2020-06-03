import socket, threading
import msg

sent_bytes = []
recv_bytes = []

def recv_loop(sock):
    print('recv thread started')
    while True:
        data = sock.recv(2048)     # receive response
        if not data:
            print('Server closing')
            break
        recv_bytes.append(len(data))

def client(server_addr):
    """Client - sending and receiving threads
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)         # connect to server process

    receiver = threading.Thread(target=recv_loop, args=(sock,))
    receiver.start()    # start recv_loop thread

    # main thread continues hereafter
    for message in msg.msgs(20, length=2000):
        n_sent = sock.send(message)
        sent_bytes.append(n_sent)
    sock.shutdown(socket.SHUT_WR)     # send FIN. This will stop receiver thread
    receiver.join()                   # wait for receiver exit
    sock.close()
    print('Client terminated')
    msg.report(sent_bytes, recv_bytes)

if __name__ == '__main__':
    client(('np.hufs.ac.kr', 7))
