# Network Programming

## docs/
- socketAPI.md: TCP Socket API
- np1.ipython: introduction to NP
- np2.md: Network programing: clients
- np3.md: Network programming: servers
- iot.ipynb: Client/Server for IoT - an example code
- http.ipynb: HTTP protocols

## intro/
- echocli.py
- echoserv.py

## echo/
### echo/clients/
- client_wrong.py: incorrect version
- client_shutdown.py: receive more data after shutdown
- client_makefile.py: converting socket to file-like object
- client_thread.py: multi-threading
- client_select.py: I/O multiplexing
- client_class.py: class implementation
- clients.py: running multiple clients for testing servers<br>
    Usage:
    ```bash
    python clients.py host:port <# of messages> [n]   # run n(=3, default) clients
    ```

### echo/servers/
- server_select0.py: I/O multiplexing version without logging and exception handling
- server_select.py: I/O multiplexing version
- server_thread.py: multi-threading version
- server.py: Generic Threading TCP server with request handlers
- server_socketserver: Threading TCP server using socketserver module

## iot/
- iotclient.py: an IoT client example
- iotserver.py: an IoT server example

## http/
- httpcli.py: http client using socket
- httpserver.py: writing HTTPHandler using socketserver.TCPServer
- headers.py: parse HTTP headers
