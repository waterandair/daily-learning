#!/usr/bin/python3
# coding utf-8
from xmlrpc.server import SimpleXMLRPCServer
"""
Perhaps the easiest way to implement a simple remote procedure call mechanism is to use 
XML-RPC.Here is an example of a simple server that implements a simple key-value store: 
"""
class KeyValueServer:
    _rpc_methods_ = ['get', 'set', 'delete', 'exists', 'keys']

    def __init__(self, address):
        self._data = {}
        self._serv = SimpleXMLRPCServer(address, allow_none=True)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self, name))

    def get(self, name):
        return self._data[name]

    def set(self, name, value):
        self._data[name] = value

    def delete(self, name):
        del self._data[name]

    def exists(self, name):
        return name in self._data

    def keys(self):
        return list(self._data)

    def server_forever(self):
        self._serv.serve_forever()


if __name__ == '__main__':
    kvserv = KeyValueServer(('', 2000))
    kvserv.server_forever()
