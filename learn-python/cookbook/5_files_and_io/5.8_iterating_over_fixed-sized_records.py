#!/usr/bin/python3
# -*- coding utf-8 -*-
from functools import partial
"""
Use the iter() function and functools.partial() using this neat trick.
"""
RECORD_SIZE = 32
with open('5.8_text_file.txt', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        print(r)

"""
A little-known feature of the iter() function is that it can create an iterator if you pass it a callable and a sentinel
value.The resulting iterator simply calls the supplied callable over and over again until it returns the sentinel,
at which point iteration stops.
"""

"""
Last, but not least,  the solution shows the file being opened in binary mode.For reading fixed-sized records,this
would probably be the most common case.
For text files,reading line by line(the default iteration behavior) is more common.
"""

