#!/usr/bin/python3
# -*- coding utf-8 -*-
import os

"""
This problem if easily solved by using the little-known x mode to open() instead of the usual w mode
"""
with open('5.5.1.txt', 'wt') as f:
    f.write('Hello\n')

with open('5.5.1.txt', 'xt') as f:
    f.write('Hello\n')

"""
Traceback (most recent call last):
  File "./5.5writing_to_a_file_that_does_not_already_exist.py", line 10, in <module>
    with open('5.5.1.txt', 'xt') as f:
FileExistsError: [Errno 17] File exists: '5.5.1.txt'\
"""

"""
An alternative solution is to first test for the file like this:
"""
if not os.path.exists('5.5.1.txt'):
    with open('5.5.1.txt', 'wt') as f:
        f.write('Hello\n')
else:
    print('File is already exists!')