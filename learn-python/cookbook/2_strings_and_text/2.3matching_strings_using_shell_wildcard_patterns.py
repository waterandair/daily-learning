#!/usr/bin/python
# -*- coding utf-8 -*-
from fnmatch import fnmatch, fnmatchcase

res = fnmatch('foo.txt', '*.txt')
print(res)  # True

res = fnmatch('foo.txt', '?oo.txt')
print(res)  # True

res = fnmatch('Dat45.csv', 'Dat[0-9]*')
print(res)  # True

names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
print([name for name in names if fnmatch(name, 'Dat*.csv')])  # ['Dat1.csv', 'Dat2.csv']

# use fnmatchcase() matches exactly based on the lower and uppercase conventions that you supply
res = fnmatchcase('foo.txt', '*.TXT')
print(res)  # False

# an often overlooked feature of these functions is their potential use with data processing of nonfilename strings

addresses = [
    '5412 N CLARK ST',
    '1060 W ADDISON ST',
    '1039 W GRANVILLE AVE',
    '2122 N CLARK ST',
    '4802 N BROADWAY',
]
res = [addr for addr in addresses if fnmatchcase(addr, '* ST')]
print(res)  # ['5412 N CLARK ST', '1060 W ADDISON ST', '2122 N CLARK ST']

res = [addr for addr in addresses if fnmatchcase(addr, '54[0-9][0-9] *CLARK*')]
print(res)  # ['5412 N CLARK ST']

# the matching performed by fnmatch sits somewhere between the functionality of simple string methods
# and the full power of regular expressions.