#!/usr/bin/python
# -*- coding utf-8 -*-

"""
A somewhat common scenario in programs involving I/O is to write code like this
"""

"""
CHUNKSIZE = 8192


def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        process_data(data)
"""

"""
Such code can often be replaced using iter() as follows：
"""
CHUNKSIZE = 8192
def reader(s):
    for chunk in iter(lambda :s.recv(CHUNKSIZE)):
        # process_data(data)
        pass