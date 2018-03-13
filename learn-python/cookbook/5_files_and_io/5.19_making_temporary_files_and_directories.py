#!/usr/bin/python3
# -*- coding utf-8 -*-
from tempfile import TemporaryFile
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory
"""
 The temporary module has a variety of functions for performing this task.
 To make an unnamed temporary file, use tempfile.TemporaryFile:
"""
with TemporaryFile('w+t') as f:
    # Read/Write to the file
    f.write('Hello world\n')
    f.write('Testing\n')

    # Seek back to begining and read the data
    f.seek(0)
    data = f.read()
    print(data)
# Temporary file if destroyed

# Or, if you prefer, you can also use the file like this:
f = TemporaryFile('w+t')
pass
f.close()


"""
On most Unix systems, the file created by TemporaryFile() is unnamed and won't even have a directory entry.
If you want to relax this constraint, use NamedTemporaryFile() instead.
"""
with NamedTemporaryFile('w+t') as f:
    print('filename is:', f.name)

"""
If you don't want deleting the file when it's closed, supply a delete=False keyword argument
"""
with NamedTemporaryFile('w+t', delete=False) as f:
    print(f.name)

"""
To make a temporary directory, use tempfile.TemporaryDirectory()
"""
with TemporaryDirectory() as dirname:
    print('dirname is : ', dirname)