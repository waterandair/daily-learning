#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
Use the open() function with mode 'rt' to read a text file.
"""
# read the entire file as a single string
with open('./test.txt', 'rt') as f:
    data = f.read()

# Iterate over the lines of the file
with open('./test.txt', 'rt') as f:
    for line in f:
        pass


"""
Similarly, to write a text file, use open() with mode 'wt' to write a file, clearing and overwriting the previous
contents(if any).
"""
# Write chunks of text data
with open('./test2.txt', 'wt') as f:
    f.write('a1')
    f.write('a2')

# Redirected print statement
with open('test3.txt', 'wt') as f:
    print('aaa', file=f)
    print('bbb', file=f)


with open('somefile.txt', 'rt', encoding='latin-1') as f:
    pass