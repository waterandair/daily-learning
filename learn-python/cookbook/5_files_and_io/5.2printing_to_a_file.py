#!/usr/bin/python3
# -*- coding utf-8 -*-
"""
Use the file keyword argument to print()
"""

with open('test4.txt', 'wt') as f:
    print('hello', file=f)

"""
There's not much more to printing to a file other than this.However, make sure that the file is opened in text mode.
Printing will fail if the underlying file is in binary mode
"""
