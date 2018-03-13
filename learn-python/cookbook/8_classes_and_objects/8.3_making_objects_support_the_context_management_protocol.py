#!/usr/bin/python3
# -*- coding utf-8 -*-
from functools import partial
from socket import socket, AF_INET, SOCK_STREAM
"""
In order to make an object compatible with the with statement, you need to implement __enter__() and __exit__() methods.
"""
class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    """
    The __exit__() method can choose to use the exception information in some way or to ignore it by doing nothing and \
    return None as a result.
    If __exit__ returns True, the exception is cleared as if nothing happened and program continues executing statement
    immediately after the "with" block
    """
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()
        self.sock = None

conn = LazyConnection(('www.python.org', 80))

with conn as s:
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))

    # print(resp)

