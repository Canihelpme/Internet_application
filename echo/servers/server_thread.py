import socket
import threading, logging

# logging.basicConfig(filename='', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(threadName)s:%(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def echo_handler(conn, cli_addr):
    try:
        while True:
            data = conn.recv(1024)  # recv next message on connected socket
            if not data:       # eof when the socket closed
                logging.info('Client closing: {}'.format(cli_addr))
                break
            logging.debug('Rcvd from {}: {} bytes'.format(cli_addr, len(data)))
            conn.send(data)         # send a reply to the client
    except Exception as e:
        logging.exception('Exception: {}'.format(e))
    finally:
        conn.close()

def echo_server(my_port):   
    """Echo server (iterative)""" 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # make listening socket
#    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse port number if used
    sock.bind(('', my_port))        # bind it to server port number
    sock.listen(5)                  # listen, allow 5 pending connects
    logging.info('Server started')
    try:
        while True:                     # do forever (until process killed)
            conn, cli_addr = sock.accept()  # wait for next client connect
                                        # conn: new socket, addr: client addr
            logging.info('Connection from {}'.format(cli_addr))
            handler = threading.Thread(target=echo_handler, args=(conn, cli_addr))
            handler.setDaemon(True)   # daemonize this thread. i.e not to wait child thread
            handler.start()
    except Exception as e:
        logging.exception('Exception at listening:'.format(e))
        sock.close()
        raise
    finally:
        sock.close()

if __name__ == '__main__':
    echo_server(10007)

