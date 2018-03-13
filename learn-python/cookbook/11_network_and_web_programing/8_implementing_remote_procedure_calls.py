#!/usr/bin/python3
# coding utf-8
import pickle
from multiprocessing.connection import Listener
from threading import Thread
"""
RPC is easy to implement by encoding function requests, arguments, and return values using pickle, and passing the 
pickled byte strings between interpreters.
"""
class RPCHandler:
    def __init__(self):
        self._functions = {}

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # receive a message
                func_name, args, kwargs = pickle.loads(connection.recv())
                try:
                    r = self._functions[func_name](*args, **kwargs)
                    connection.send(pickle.dumps(r))
                except Exception as e:
                    connection.send(pickle.dumps(e))
        except EOFError:
            pass

"""
To use this handler, you need to add it into a messaging server.There are many possible choices, but the multiprocessing
library provides a simple option.
"""
def rpc_server(handler, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client, ))
        t.daemon = True
        t.start()

# some remote functions
def add(x, y):
    return x + y


def sub(x, y):
    return x - y


# register with a handler
handler = RPCHandler()
handler.register_function(add)
handler.register_function(sub)

# run the server
rpc_server(handler, ('127.0.0.1', 2000), authkey=b'000000')