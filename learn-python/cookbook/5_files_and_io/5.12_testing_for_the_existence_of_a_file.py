#!/usr/bin/python3
# -*- coding utf-8 -*-
import os
import time
"""
Use the os.path module to test for the existence of a file or directory
"""
print(os.path.exists('/etc/passwd'))  # Ture
print(os.path.exists('/tmp/spam'))  # False

# is a regular file
print(os.path.isfile('/etc/passwd'))  # True
# is a directory
print(os.path.isdir('/etc/passwd'))  # False

# is a symbolic link
print(os.path.islink('/usr/bin/python3'))  # True

# get the file linked to
print(os.path.realpath('/usr/bin/python3'))  # /usr/bin/python3.5


"""
If you need to get metadata (the file size or modification date), that is also available in the os.path.module
"""
print(os.path.getsize('/etc/passwd'))  # 2611

print(os.path.getmtime('/etc/passwd'))  # 1511102759.2567306

print(time.ctime(os.path.getmtime('/etc/passwd')))  # Sun Nov 19 22:45:59 2017