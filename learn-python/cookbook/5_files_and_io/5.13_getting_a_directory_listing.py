#!/usr/bin/python3
# -*- coding utf-8 -*-
import os
import os.path
import glob
from fnmatch import fnmatch
"""
Use the os.listdir() function to obtain a list of files in a directory
"""
name = os.listdir('./')
print(type(name))  # <type 'list'>

"""
This will give you the raw directory listing, including all files, subdirectories, symbolic links, and so forth.
If you need to filter the data in some way, consider using a list comprehension combined with various functions
in the os.path library.
"""
# get all regular files
names = [name for name in os.listdir('./') if os.path.isfile(os.path.join('./', name))]

# get all dirs
dirnames = [name for name in os.listdir('./') if os.path.isdir(os.path.join('./', name))]

"""
The startswith() and endswith() methods of strings can be useful for filtering the contents of a directory as well.
"""
pyfiles = [name for name in os.listdir('./') if name.endswith('.py')]


"""
For filename matching, you may want to use the glob or fnmatch modules instead
"""
pyfiles = glob.glob('./*.py')

pyfiles = [name for name in os.listdir('./') if fnmatch(name, '*.py')]

# get file sizes and modification dates
name_sz_date = [(name, os.path.getsize(name), os.path.getmtime(name)) for name in pyfiles]

for name, size, mtime in name_sz_date:
    print(name, size, mtime)


# Alternative: get file metadata
file_metadata = [(name, os.stat(name)) for name in pyfiles]
for name, meta in file_metadata:
    print(name, meta.st_size, meta.st_mtime)