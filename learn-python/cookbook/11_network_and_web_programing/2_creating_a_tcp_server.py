#!/usr/bin/python3
# coding utf-8
from socketserver import BaseRequestHandler, TCPServer, StreamRequestHandler, ThreadingTCPServer
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
"""
A easy way to create a TCP server is to use the socketserver library.
"""


class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('got connection from ', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)


"""
In many cases, it may be easier to define a slightly different kind of handler.
Here is an example that uses the StreamRequestHandler base class to put a file-like
interface on underlying socket
"""
class EchoHandler2(StreamRequestHandler):
    def handle(self):
        print('got connection from ', self.client_address)
        for line in self.rfile:
            self.wfile.write(line)


"""
The streamRequestHandler class is actually a bit more flexible, and supports some features that can be enabled 
through the specification of additional class variables.
"""
class EchoHandler3(StreamRequestHandler):
    # optional settings
    timeout = 5
    rbufsize = -1  #  read buffer size
    wbufsize = 0  # write buffer size
    disable_nagle_algorithm = False  # sets TCP_NODELAY socket option

    def handle(self):
        print('got connection from ', self.client_address)
        try:
            for line in self.rfile:
                self.wfile.write(line)
        except socket.timeout:
            print('Timed out')


"""
It is also not difficult to implement servers directly using the socket library as well.
Here is a simple example of directly programming a server with socket
"""
def echo_handler(address, client_sock):
    print('got connection from {}'. format(address))
    while True:
        msg = client_sock.recv(1024)
        if not msg:
            break
        client_sock.sendall(msg)
    client_sock.close()


def echo_server(address, backlog=5):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)
    while True:
        client_sock, client_addr = sock.accept()
        echo_handler(client_addr, client_sock)


if __name__ == '__main__':
    serv = TCPServer(('', 2001), EchoHandler)
    """
    If you want to handle multiple clients, either instantiate a ForkingTCPServer
    or ThreadingTCPServer object instead
    """
    # serv = ThreadingTCPServer(('', 2001), EchoHandler)
    serv.serve_forever()

    """
    You can create a pre-allocated pool of worker threads or process to avoid hacker attacks
    """
    # NWORKERS = 16
    # serv = TCPServer(('', 2000), EchoHandler)
    # for n in range(NWORKERS):
    #     t = Thread(target=serv.serve_forever)
    #     t.daemon = True
    #     t.start()
    # serv.serve_forever()


    """
    Normally, a TCPServer binds and actives the underlying socket upon instantiation.
    However, sometimes you might want to adjust the underlying socket by setting options.
    To do this, supply the bind_and_activate = False argument 
    """
    # serv = TCPServer(('', 2000), EchoHandler, bind_and_activate=False)
    # # set up various socket options
    # serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # # Bind and activate
    # serv.server_bind()
    # serv.server_activate()
    # serv.serve_forever()

    """
    The socket option shown is actually a very common setting that allows the server to rebind to a previously used port
    number.It's actually so common it's a class variable that can be set on TCPServer.
    Set it before instantiating the server, as shown in this example: 
    """
    # TCPServer.allow_reuse_address = True
    # serv = TCPServer(('', 2000), EchoHandler)
    # serv.serve_forever()


    # echo_server(('', 2000))


