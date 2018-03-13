#!/usr/bin/python3
# -*- coding utf-8 -*-
import os.path
"""
You want to read binary data directly into a mutable buffer without any intermediate copying.Perhaps you want to
mutate the data in-place and write it back out a file.
"""

"""
To read data into a mutable array,use the readinto() method of files.
"""


def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf


"""example"""
with open('5.8sample.bin', 'wb') as f:
    f.write(b'Hello world')

buf = read_into_buffer('./5.8sample.bin')
print(buf)  # bytearray(b'Hello world')
buf[0:5] = b'Hi'
print(buf)  # bytearray(b'Hi world')

with open('5.9_new_sample.bin', 'wb') as f:
    f.write(buf)


"""
The readinto() method of files can be used to fill any preallocated array with data.This even includes arrays created 
from the array module or libraries such as numpy. 
Unlike the normal read() method,readinto() fills the contents of an existing buffer rather than allocating new objects
and returning them.
Thus, you might be able to use it to avoid making extra memory allocations.
For example, if you are reading a binary file consisting of equally sized records,you can write code like this:
"""
record_size = 32
buf = bytearray(record_size)
with open('5.9_new_sample.bin', 'rb') as f:
    while True:
        n = f.readinto(buf)
        if n < record_size:
            break


"""
Another interesting feature to use here might be a memoryview, which lets you make zero-copy slices of an existing 
buffer and even change its contents
"""
buf = bytearray(b'hello world')
m1 = memoryview(buf)
m2 = m1[-5:]
print(m2)  # <memory at 0x7f7d324e01c8>
m2[:] = b'WORLD'
print(buf)  # bytearray(b'hello WORLD')

"""
Finally, be on the lookout for other "into" related functions in various library modules(recv_into(), pack_into())
Many other parts of Python have support for direct I/O or data access that can be used to fill or alter the contents
of arrays and buffers
"""