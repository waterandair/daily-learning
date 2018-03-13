#!/usr/bin/python3
# coding utf-8
from socketserver import BaseRequestHandler, UDPServer
import time
from socket import socket, AF_INET, SOCK_DGRAM
"""
As with TCP, UDP servers are also easy to create using the socketserver library.
"""

class TimeHandler(BaseRequestHandler):
    def handle(self):
        print('got connection from ', self.client_address)
        # get message and client socket
        msg, sock = self.request
        resp = time.ctime()
        sock.sendto(resp.encode('ascii'), self.client_address)


"""
Implementing a UDP server directly using sockets is also not diffcult.
"""
def time_server(address):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(address)
    while True:
        msg, addr = sock.recvfrom(1024)
        print('got message from ', addr)
        res = time.ctime()
        sock.sendto(res.encode('ascii'), addr)



if __name__ == '__main__':
    serv = UDPServer(('', 2000), TimeHandler)
    serv.serve_forever()

    # time_server(('', 2000))
