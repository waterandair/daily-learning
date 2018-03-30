#!/usr/bin/python
# -*- coding utf-8 -*-
import re

# The strip() method can be used to strip characters from the beginning or end of a string.lstrip() and rstrip() perform
# stripping form the left or right side,respectively.
# By default, these methods strip whitespace, but other characters can be given

s = '    hello world   \n'
res = s.strip()
print(res)  # 'hello world'

res = s.lstrip()
print(res)  # 'hello world   \n'

res = s.rstrip()
print(res)  # '    hello world'


t = '-----hello====='
res = t.lstrip('-')
print(res)  # hello=====

res = t.strip('-=')
print(res)  # hello

# Be aware that stripping does not apply to any text in the middle of a string


# If you needed to do something to the inner space, you would need to use another technique, such as using the
# replace() method or a regular expression substitution.
s = '  hello       world   \n'

res = s.replace(' ', '')
print(res)  # helloworld

res = re.sub('\s+', ' ', s)
print(res)  # ' hello world'

# It's efficient because it doesn't actually read the data into any kind of temporary list first.
with open('test.txt', 'r') as f:
    lines = (line.strip() for line in f)
    for line in lines:
        print(line)
