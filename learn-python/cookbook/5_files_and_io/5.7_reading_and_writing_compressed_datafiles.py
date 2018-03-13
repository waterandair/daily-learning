#!/usr/bin/python3
# -*- coding utf-8 -*-
import gzip
import bz2
"""
The gzip and bz2 modules make it easy to work with such files.Both modules provide an alternative implementation of open()
that can be used for this purpose.
"""
# gzip compression
with gzip.open('./5.7_test.txt.gz', 'rt') as f:
    text = f.read()
    print(text)

"""
test5.7 gzip 
hahaha
"""
# bz2 compression
with bz2.open('./5.7_testbz.txt.bz2', 'rt') as f:
    text = f.read()
    print(text)
"""
5.7test
bz2
"""


"""
Similarly. to write compressed data, do this:
"""
with gzip.open('5.7_test_write.txt.gz', 'wt') as f:
    f.write('5.7_test_write.txt.gz')

with bz2.open('5.7_test_write.txt.bz2', 'wt') as f:
    f.write('5.7_test_write.txt.bz2')


"""
When writing compression data, the compression level can be optionally specified using the compresslevel 
keyword argument.
"""
with gzip.open('5.7_text_compresslevel.gz', compresslevel=5) as f:
    f.write('5.7_text_compresslevel.gz')

"""
The default level is 9, which provides the highest level of compression.
"""