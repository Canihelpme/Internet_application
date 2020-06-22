import sys, socket

def echo_client(server_addr):
    """Echo client"""
    # make TCP/IP socket obj
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET이라는 것이 socket version4  SOCK_STREAM이 TCP소켓 정의.
    sock.connect(server_addr)   # connect to server process
    print(sock)
    while True:
        message = sys.stdin.readline()
        if not message:     # reading 0 bytes means EoF
            break
        sock.send(message.encode('utf-8'))      # send message to server #실상보면 이건 전송과관련 없음. 그저 kernel에 보내는거고 보내는것이 성공적으로 되면 이건 send라는 버퍼에 저장이 되었다라고 말해주는 것일 뿐
        data = sock.recv(1024).decode('utf-8')  # receive response up to 1KB
        #print(data, end='')
    sock.close()                # send FIN(no more data) and close the socket
    
if __name__ == '__main__':
    echo_client(('localhost', 10007))
    # echo_client(('np.hufs.ac.kr', 7))

