import socket, sys, threading
import msg

class Client(threading.Thread):
    """Supports concurrent clients with multi-threading

    outgoing stream: using socket
    incoming stream: using file-like object (buffered)
                     assuming response messages are separated by new line
    """
    def __init__(self, server_addr, n_mesg):
        threading.Thread.__init__(self)

        self.n_mesg = n_mesg
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_addr)
        print(f'Connected to server: {server_addr}')
        # convert socket to file-like obj only for imcoming messages
        self.rfile = self.sock.makefile('rb')

    def run(self):
        print(f'{self.getName()} starts')
        for message in msg.msgs(n_mesg, length=2000):
            n_sent = self.sock.send(message)
            print(f'send {n_sent} bytes')
            data = self.rfile.readline()      # receive response
            if not data:
                print('Server closing')
                break
            print(f'recv {len(data)} bytes')
        self.sock.close()                     # to send eof to server

if __name__ == '__main__':
    usage = 'Usage: python clients.py host:port <# of msgs> [<# of clients>]'
    n_clients = 3
    try:
        if len(sys.argv) in (3, 4):
            host, port = sys.argv[1].split(':')
            port = int(port)
            n_mesg = int(sys.argv[2])
            if len(sys.argv) == 4:
                n_clients = int(sys.argv[2])
        else:
            print(usage)
    except Exception as e:
        print(usage)
        raise
    # create and start n client thread objects
    threads = []
    for i in range(n_clients):
        cli = Client((host, port), n_mesg)
        cli.start()
        threads.append(cli)

    # Wait for child threads to terminate
    for t in threads:
        t.join()        # wait for child thread t
        print(f'{t.getName()} exits')

