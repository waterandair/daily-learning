#!/usr/bin/python
# -*- coding utf-8 -*-
import re

text = 'yeah, but no, but yeah, but no, but yeah'
res = text == 'yeah'
print(res)  # False

res = text.startswith('yeah')
print(res)  # True

res = text.endswith('no')
print(res)  # False

res = text.find('no')
print(res)  # 10

# For more complicated matching, use regular expressions and the re module.

text1 = '11/27/2012'
text2 = 'Nov 27, 2012'

if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')

if re.match(r'\d+/\d+/\d+', text2):
    print('yes')
else:
    print('no')

# if you're going to perform a lot of matches using the same pattern, it usually pays to precompile the
# regular expression pattern into a pattern object first.

datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')

if datepat.match(text2):
    print('yes')
else:
    print('no')

# match() always tries to find the match at the start of a string. If you want to search text for all occurrences
# of a pattern, use the findall() method instead

text = 'Today is 11/27/2012. PyCon starts 3_num_date_time/13/2013.'
print(datepat.findall(text))  # ['11/27/2012', '3_num_date_time/13/2013']

# when defining regular expression, it is common to introduce capture groups by enclosing parts of the pattern in
# parentheses

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
m = datepat.match('11/27/2012')
print(m)  # <_sre.SRE_Match object at 0x7f2886c6a918>
print(m.group(0))  # 11/27/2012
print(m.group(1))  # 11
print(m.group(2))  # 27
print(m.group(3))  # 2012
print(m.groups())  # ('11', '27', '2012')

print(datepat.findall(text))  # [('11', '27', '2012'), ('3_num_date_time', '13', '2013')]

# the findall() method searches the text sand finds all matches, returning them as a list.
# if you want to find matches iteratively, use the finditer() method instead.

res = datepat.finditer(text)
print(res)  # <callable-iterator object at 0x7f83a916f410>

for m in datepat.finditer(text):
    print(m.groups())