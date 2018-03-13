#!/usr/bin/python3
# coding utf-8
from xmlrpc.client import ServerProxy
s = ServerProxy('http://127.0.0.1:2000', allow_none=True)
s.set('foo', 'bar')
s.set('spam', [1, 2, 3])
print(s.keys())

print(s.get('foo'))