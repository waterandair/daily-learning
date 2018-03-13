#!/usr/bin/python3
# -*- coding utf-8 -*-
import os
import fnmatch
import gzip
import bz2
import re

"""
You want to process data iteratively in the style of a data processing pipeline(similar to unix pipes).
For instance, you have a huge amount of data that needs to be processed,but it can't fit entirely into memory
"""


def gen_find(filepat, top):
    """
    Find all filenames in a directory tree that match a shell wildcard pattern
    :param filepat: 
    :param top: 
    :return: 
    """
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def gen_opener(filenames):
    """
    Open a sequence of filenames one at a time producing a file object.The file is closed immediately when processing to
    the next iteration
    :param filename:
    :return:
    """
    for filename in filenames:
        if filename.endswith('.py'):
            f = open(filename, 'r')
            yield f
            f.close()


def gen_concatenate(iterators):
    """
    chain a sequence of iterators together into a single sequence
    :param iterators:
    :return:
    """
    for it in iterators:
        yield from it


def gen_grep(pattern, lines):
    """
    Look for a regex pattern in a sequence of lines
    :param pattern:
    :param lines:
    :return:
    """
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line


filenames = gen_find('*.py', '../')
files = gen_opener(filenames)
lines = gen_concatenate(files)
match_lines = gen_grep('python', lines)
for i in match_lines:
    print(i)


"""!!!
Processing data in a pipelined manner works well for a wide variety of other problems, including parsing,reading from 
real-time data sources,periodic polling, and so on.
The memory efficiency of this approach can also not be overstated.The code shown would still work even if used on a 
massive directory of files.In fact, due to the iterative nature of the processing, very little memory would be used 
at all
"""
