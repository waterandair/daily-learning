#!/usr/bin/python3
# coding utf-8
from multiprocessing.connection import Listener
import traceback
"""
It is easy to communicate between interpreters if you use the multiprocessing.connection module
"""
def echo_client(conn):
    try:
        while True:
            msg = conn.recv()
            conn.send(msg)
    except EOFError:
        print('connection closed')


def echo_server(address, authkey):
    serv = Listener(address, authkey=authkey)
    while True:
        try:
            client = serv.accept()
            echo_client(client)
        except Exception:
            traceback.print_exc()

echo_server(('', 2000), authkey=b'000000')
