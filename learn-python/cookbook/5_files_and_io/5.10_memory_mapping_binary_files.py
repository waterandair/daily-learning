#!/usr/bin/python3
# -*- coding utf-8 -*-
import os
import mmap
"""
Use the mmap module to memory map files. Here is a utility function that shows how to open a file and memory map it
in a portable manner：
"""


def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)


"""
To use this function, you would need to have a file already created and filled with data.
"""

size = 1000000
with open('data', 'wb') as f:
    f.seek(size - 1)
    f.write(b'\x00')


"""
Here is an example of memory mapping the contents using the memory_map() function
"""
m = memory_map('data')
print(len(m))  # 1000000

print(m[0:10])  # b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

print(m[0])  # 0

# reassign a slice
m[0:11] = b'hello World'
m.close()

# Verify that changes were made
with open('data', 'rb') as f:
    print(f.read(11))  # b'hello World'

"""
The mmap object returned by mmap() can also be used as a context manager, in which case the underlying file is closed
automatically
"""

with memory_map('data') as m:
    print(len(m))  # 1000000
    print(m[0:10])  # b'hello Worl'

print(m.closed)  # True


"""
By default, the memory_map() function shown opens a file for both reading and writing. Any modifications made to he 
data are copied back to the original file.
If read-only access is needed instead, supply mmap.ACCESS_READ for the access argument.
"""
m = memory_map('data', mmap.ACCESS_READ)

"""
If you intend to modify the data locally, but don't want those changes written back to the original file, use 
mmap.ACCESS_COPY
"""
m = memory_map('data', mmap.ACCESS_COPY)