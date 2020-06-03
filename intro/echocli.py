import sys, socket

def echo_client(server_addr):
    """Echo client"""
    # make TCP/IP socket obj
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)   # connect to server process
    print(sock)
    while True:
        message = sys.stdin.readline()
        if not message:
            break
        sock.send(message.encode('utf-8'))      # send message to server
        data = sock.recv(1024).decode('utf-8')  # receive response up to 1KB
        print(data)
    sock.close()                # send FIN(no more data) and close the socket
    
if __name__ == '__main__':
    echo_client(('localhost', 10007))
    # echo_client(('np.hufs.ac.kr', 7))

