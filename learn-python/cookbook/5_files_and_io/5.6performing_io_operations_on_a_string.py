#!/usr/bin/python3
# -*- coding utf-8 -*-
import io

"""
You want to feed a text or binary string to code that's been written to operate on file-like objects instead
"""

"""
Use the io.stringIO and io.BytesIo classes to create file-like objects that operate on string data.
"""
s = io.StringIO()
s.write('Hello worlddddd\n')
print('This is a test', file=s)

print(s.getvalue())
"""
Hello worlddddd
This is a test
"""

# wrap a file interface around an existing string
s = io.StringIO('Hello\nWorld\n')
print(s.read(4))
print(s.read())

"""
The io.StringIo class should only be used for text.If you are operating with binary data,use the io.BytesIo class instead
"""
s = io.BytesIO()
s.write(b'binary data')
print(s.getvalue())


"""
The StringIO and BytesIo classes are most useful in scenarios where you need to mimic a normal file for some reason.
For example,in unit tests,you might use StringIO to create a file-like object containing test data that's fed into a 
function that would otherwise work with a normal file
Be aware that StringIO and BytesIO instances don't have a proper integer file-descriptor. Thus. they do not work with 
code that requires the use of a real system-level file such as a file, pipe, or socket.
"""
