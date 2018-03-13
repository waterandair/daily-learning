#!/usr/bin/python3
# coding utf-8
from multiprocessing.connection import Client
c = Client(('127.0.0.1', 2000), authkey=b'000000')
c.send('hello')
print(c.recv())