"""Serve only one client at a time
"""

from socket import socket, AF_INET, SOCK_STREAM

def echo_server(my_port):   
    """Echo Server - iterative"""

    sock = socket(AF_INET, SOCK_STREAM) # socket for listening clients' connection
    sock.bind(('', my_port))        # bind it to my any IP and port number
                                    # '' represents all available interfaces on host
    sock.listen(5)                  # listen, allow 5 pending connects
    print('Server started')
    while True:                     # do forever (until process killed)
        conn, cli_addr = sock.accept()  # wait for next client connect
                                    # conn: new socket, addr: client addr
        print(conn)
        print('Connection from', cli_addr)
        while True:
            data = conn.recv(1024)  # recv next message on connected socket
            if not data:
                break               # no more data. TCP FIN arrival
            print(data.decode(), end='')
            conn.send(data)         # send a reply to the client
        print('Client closed', cli_addr)
        conn.close()               # close the connected socket
        
if __name__ == '__main__':
    echo_server(10007)

