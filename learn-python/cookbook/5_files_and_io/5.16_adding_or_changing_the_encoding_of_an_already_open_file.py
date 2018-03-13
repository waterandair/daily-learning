#!/usr/bin/python3
# -*- coding utf-8 -*-
import urllib.request
import io
import sys

"""
If you want to add Unicode encoding/decoding to an already existing file object that's opened in 
binary mode,
wrap it with an io.TextIOWrapper() object
"""
u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u, encoding='gbk')
text = f.read()
print(text)

"""
If you want to change the encoding of an already open 
text-mode
file, use its detach() method to remove the existing text encoding layer before replacing it with a new one.
"""
print(sys.stdout.encoding)  # UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
print(sys.stdout.encoding)  # latin-1


"""
The I/O system is built as a series of layers. You can see the layers yourself by trying this simple example
"""
f = open('5.16_sample.txt', 'w')
print(f)  # <_io.TextIOWrapper name='5.16_sample.txt' mode='w' encoding='UTF-8'>
print(f.buffer)  # <_io.BufferedWriter name='5.16_sample.txt'>
print(f.buffer.raw)  # <_io.FileIO name='5.16_sample.txt' mode='wb' closefd=True>

"""
In this example, io.TextIOWrapper is a text-handling layer that encodes and decodes Unicode,
io.BufferedWriter is a buffered I/O layer that handles binary data
io.FileIO is a raw file representing the low-level file descriptor in the operating system.
Adding or changing the text encoding involves adding or changing the topmost io.TextWrapper layer.

As a general rule, it's not safe to directly manipulate the different layers by accessing the attributes shown.
For example, see what happens if you try to change the encoding using this technique
"""
print(f)  # <_io.TextIOWrapper name='5.16_sample.txt' mode='w' encoding='UTF-8'>
f = io.TextIOWrapper(f.buffer, encoding='latin-1')
print(f)  # <_io.TextIOWrapper name='5.16_sample.txt' encoding='latin-1'>
f.write('Hello')
# Traceback (most recent call last):
#   File "./5.16_adding_or_changing_the_encoding_of_an_already_open_file.py", line 47, in <module>
#     f.write('Hello')
# ValueError: I/O operation on closed file.

"""
It doesn't work because the original value of f got destroyed and closed the underlying file in the process.
The detach() method disconnects the topmost layer of a file and returns the next lower layer.
Afterward, the top layer will no longer be usable.
"""

"""
Although changing the encoding has been shown, it is also possible to use this technique to change the line
handing, error policy,and other aspects of file handing
"""
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='ascii', errors='xmlcharrefreplace')
# print('Jalape\u00f1o')  # Jalape&#241;o
