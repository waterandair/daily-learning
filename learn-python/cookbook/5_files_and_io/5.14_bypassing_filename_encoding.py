#!/usr/bin/python3
# -*- coding utf-8 -*-
import sys
import os
"""
You want to perform file I/O operations using raw filenames that have not been decoded or encoded according to
the default filename encoding.
"""

"""
By default, all filenames are encoded and decoded according to the text encoding returned by
sys.getfilesystemencoding()
"""
print(sys.getfilesystemencoding())  # UTF-8

"""
If you want to bypass this encoding for some reason, specify a filename using a raw byte string(原始字节字符串) instead
"""
# write a file using a unicode filename
with open('jialape\xf1o.txt', 'w') as f:
    f.write('Spicy!')

# Directoty listing(decoded)
print(os.listdir('.'))

# Directory listing (raw)
print(os.listdir(b'.'))

# Open file with raw filename
with open(b'jialape\xc3\xb1o.txt') as f:
    print(f.read())  # Spicy!

"""
As you can see in the last two operations , the filename handing changes ever so slightly when byte strings
are supplied when byte string are supplied to file-related functions, such as open() and os,listdir()
"""
