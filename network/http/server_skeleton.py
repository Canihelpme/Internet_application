"""Serve only one client at a time
"""
import socket, socketserver, time
import mimetypes   # for map filenames to MIME types
import headers

def request_handler(rfile, wfile):
    while True:
        # read request message
        method, path, protocol = rfile.readline().decode().split()
        req_headers = headers.parse_headers(rfile)
        content_length = req_headers.get('Content-length')
        if content_length:      # if request body exists
            body = rfile.read(int(content_length))
        else:
            body = None
        print(method, path, protocol)
        print(req_headers)
        if content_length:
            print(body)

        # Build response message
        import os
        file = '.' + path
        try:
            f = open(file, 'rb')
        except:
            content = None
        else:
            content = f.read()
            f.close()
        if content:
            print('HTTP/1.1 200 OK')
            wfile.write(b'HTTP/1.1 200 OK\r\n')
        else:
            print('HTTP/1.1 404 not found')
            wfile.write(b'HTTP/1.1 404 not found\r\n')
        res_headers = {}
        res_headers['Date'] = time.asctime()
        res_headers['Server'] = 'MyServer/1.0'
        res_headers['Accept-Ranges'] = 'bytes'
        if req_headers.get('Connection') == 'close':
            res_headers['Connection'] = 'close'
        else:
            res_headers['Connection'] = 'keep-alive'
        if content:
            content_type, encoding = mimetypes.guess_type(file)
            res_headers['Content-type'] = content_type
            res_headers['Content-length'] = str(len(content))
        res_headers_text = headers.to_bytes(res_headers)
        print(res_headers_text.decode())
        wfile.write(res_headers_text)
        if content:
            wfile.write(content)
        wfile.flush()
        if res_headers['Connection'] == 'close':
            break

def echo_server(my_port):   
    """Echo Server - iterative"""

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket for listening clients' connection
    server_sock.bind(('', my_port))        # bind it to my any IP and port number
                                    # '' represents all available interfaces on host
    server_sock.listen(5)                  # listen, allow 5 pending connects
    print('Server started')
    while True:                     # do forever (until process killed)
        conn, cli_addr = server_sock.accept()  # wait for next client connect
                                    # conn: new socket, addr: client addr
        print('Connection from', cli_addr)
#        conn.settimeout(5)
        rfile = conn.makefile('rb')
        wfile = conn.makefile('wb')
        request_handler(rfile, wfile)
        rfile.close()
        wfile.close()
        print('Client closed', cli_addr)
        conn.close()               # close the connected socket
        
if __name__ == '__main__':
    echo_server(10007)

