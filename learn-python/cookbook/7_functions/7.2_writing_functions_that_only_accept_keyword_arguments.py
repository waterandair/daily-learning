#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
This feature is easy to implement if you place the keyword arguments after a * argument or a single unnamed *
"""

def recv(maxsize, *, block):
    'Receives a message'
    pass

# recv(1024, True)  # TypeError
recv(1024, block=True)

"""
This technique can also be used to specify keyword arguments for functions that accept a varying number of positional 
arguments.
"""
def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

minimum(1, 5, 2, -5, 10)          # Returns -5
minimum(1, 5, 2, -5, 10, clip=0)  # Returns 0

def show_input(a, *b, c, **d):
    print(a)
    print(b)
    print(c)
    print(d)

show_input('a', 'b', 'c', 'd', e='e', f='f', c='c')
"""
a
('b', 'c', 'd')
c
{'e': 'e', 'f': 'f'}
"""