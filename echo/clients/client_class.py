import socket
import msg

class Client:
    """Client - OOP
    outgoing: socket
    incoming: file-like object (buffering)
    """
    def __init__(self, server_addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_addr)      # connect to server process
        # convert socket to file-like obj only for imcoming messages
        self.in_file = self.sock.makefile('rb')
        self.sent_bytes = []
        self.recv_bytes = []

    def run(self):
        for message in msg.msgs(20, length=2000, delay=0.5):
            n_sent = self.sock.send(message)
            self.sent_bytes.append(n_sent)
            data = self.in_file.readline() # receive response
            if not data:
                print('Server closing')
                break
            self.recv_bytes.append(len(data))
        self.sock.close()                    # to send eof to server
        msg.report(self.sent_bytes, self.recv_bytes)

if __name__ == '__main__':
    cli = Client(('np.hufs.ac.kr', 7))
    cli.run()
