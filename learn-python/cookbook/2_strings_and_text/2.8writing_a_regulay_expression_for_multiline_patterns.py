#!/usr/bin/python
# -*- coding utf-8 -*-
import re

# This problem typically arises in patterns that use the dot(.) to match any character but forget to account for the
# fact that it doesn't match newlines.

# For example, suppose you are trying to match C-style comments:
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a
            multiline comment */
'''

res = comment.findall(text1)
print(res)  # [' this is a comment ']

res = comment.findall(text2)
print(res)  # []

# to fix the problem, you can add support for newlines.
# comment = re.compile(r'/\*(?:.|\n)*?\*/')
comment = re.compile(r'/\*(?:.|\n)*\*/')
res = comment.findall(text2)
print(res)  # ['/* this is a\n            multiline comment */']


# ! The re.compile() function accepts a flag, re.DOTALL, which is useful here. It makes the . in a regular expression
# match all characters, including newlines
comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
res = comment.findall(text2)
print(res)  # [' this is a\n            multiline comment ']
