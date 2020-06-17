"""
Echo server - multi-threading version
"""

import socket
import threading, logging

logging.basicConfig(filename='', level=logging.DEBUG, 
    format='%(asctime)s:%(threadName)s:%(message)s')

def echo_handler(conn, cli_addr):
    try:
        while True:
            data = conn.recv(1024)  # recv next message on connected socket
            if not data:       # eof when the socket closed
                logging.info(f'Client closing: {cli_addr}')
                break
            logging.debug(f'Rcvd from {cli_addr}: {len(data)} bytes')
            conn.send(data)         # send a reply to the client
    except Exception as e:
        logging.exception(f'echo_handler for {cli_addr}: {e}')
    finally:
        conn.close()

def echo_server(my_port):   
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # make listening socket
#    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse port number if already used
    sock.bind(('', my_port))        # bind it to server port number
    sock.listen(5)                  # listen, allow 5 pending connects
    logging.info(f'Server started: {sock.getsockname()}')
    try:
        while True:                     # do forever (until process killed)
            conn, cli_addr = sock.accept()  # wait for next client connect
                                        # conn: new socket, addr: client addr
            logging.info('Connection from: {}'.format(cli_addr))
            handler = threading.Thread(target=echo_handler, args=(conn, cli_addr))
            handler.setDaemon(True)   # Exiting main thread will cause stopping child threads
            handler.start()
    except OSError as e:
        logging.exception(f'Listening socket error: {e}')
        sock.close()
        raise
    finally:
        sock.close()

if __name__ == '__main__':
    echo_server(10007)

