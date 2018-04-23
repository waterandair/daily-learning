#!/usr/bin/python
# -*- coding utf-8 -*-
import re
# this problem often arises in patterns that try to match text enclosed inside a pair of starting and ending delimiters.
# the * operator in a regular expression is greedy
str_pat = re.compile(r'\"(.*)\"')

text1 = 'Computer says "no."'

res = str_pat.findall(text1)
print(res)  # ['no.']

text2 = 'Computer says "no." Phone says "yes."'
res = str_pat.findall(text2)
print(res)  # ['no." Phone says "yes.']

# To fix this, add the ? modifier after the * operator in the pattern, like this:
str_pat = re.compile(r'\"(.*?)\"')
# This makes the matching nongreedy, and produces the shortest match instead
res = str_pat.findall(text2)
# Adding the ? right after operators such as * or + forces the matching algorithm to look for the shortest possible
# match instead
print(res)  # ['no.', 'yes.']

