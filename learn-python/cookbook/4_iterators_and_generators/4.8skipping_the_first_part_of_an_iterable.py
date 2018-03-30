#!/usr/bin/python3
# -*- coding utf-8 -*-

from itertools import dropwhile
from itertools import islice
with open('test.txt') as f:
    for line in f:
        print(line, end=' ')

"""
 q
 ew
 e
 r
 rt
 t
 yt
 gb
 f
"""

with open('test.txt') as f:
    for line in dropwhile(lambda line: line.startswith('q'), f):
        print(line)
"""
ew
e
r
rt
t
yt
gb
f
"""
print("****************")
items = ['a', 'b', 'c', 1, 4, 10, 15]
for x in islice(items, 3, None):
    print(x)

"""
1
4
10
15
"""
print()
for x in islice(items, 3, 5):
    print(x)

"""
1
4
"""
