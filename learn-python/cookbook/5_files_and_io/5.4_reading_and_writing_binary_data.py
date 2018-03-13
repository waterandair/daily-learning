#!/usr/bin/python3
# -*- coding utf-8 -*-
import array
"""
Use the open() function with mode 'rb' or 'wb' to read or write binary data, and so on
"""
with open('./text5.bin', 'wb') as f:
    f.write(b'hello world')

with open('./text5.bin', 'rb') as f:
    print(f.read())  # b'hello world'


"""
When reading binary data, the subtle semantic differences between byte strings and text strings pose a potential gotcha.
In particular, be aware that indexing and iteration return integer byte values instead of byte strings
"""
# Text string
t = 'Hello'
print(t[0])  # H

for c in t:
    print(c)
# H
# e
# l
# l
# o

# Byte string
b = b'Hello'
print(b[0])  # 72
for b in b:
    print(b)
# 72
# 101
# 108
# 108
# 111

"""
If you ever need to read or write text from a binary-mode file, make sure you remember to decode or encode it
"""
with open('text5.bin', 'rb') as f:
    data = f.read(5)
    print(data)  # b'hello'
    print(data.decode('utf-8'))  # hello

with open('test6.bin', 'wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))


"""!!!
A lesser-known aspect of binary I/O is that objects such as arrays and C structures can be used for writing without any
kind of intermediate conversion to a bytes object
"""
nums = array.array('i', [1, 2, 3, 4])
print(nums)
with open('data.bin', 'wb') as f:
    f.write(nums)
"""
This applies to any object that implements the so-called"buffer interface", which directly exposes an underlying memory
buffer to operations that can work with it.
Writing binary data si one such operation 
"""
"""
Many objects also allow binary data to be directly read into their underlying memory using the readinto() method of 
lines
"""
a = array.array('i', [0, 0, 0, 0, 0, 0, 0, 0])
with open('data.bin', 'rb') as f:
    f.readinto(a)

print(a)  # array('i', [1, 2, 3, 4, 0, 0, 0, 0])





