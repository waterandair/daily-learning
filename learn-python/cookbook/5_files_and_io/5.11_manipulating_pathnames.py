#!/usr/bin/python
# -*- coding utf-8 -*-
import os

"""
To manipulate pathnames, use the functions in the os.path module.
"""

path = '/Users/beazley/Data/data.csv'

# get the last component of the path
print(os.path.basename(path))  # data.csv

# get the directory name
print(os.path.dirname(path))  # /Users/beazley/Data

# Join path components together
print(os.path.join('tmp', 'data', os.path.basename(path)))  # tmp/data/data.csv

# Expand the user's home directory
path = '~/Data/data.csv'
print(os.path.expanduser(path))  # /home/zj/Data/data.csv

# split the file extension
print(os.path.splitext(path))  # ('~/Data/data', '.csv')

"""
For any manipulation of filenames, you should use the os.path module instead of trying to cook up your own code
using the standard operations.
In part, this is for portability.
The os.path module knows about differences between unix and windows and can reliably deal with filenames such as
Data/data.csv and Data\data.csv.
Second, you really shouldn't spend your time reinventing the wheel.
"""