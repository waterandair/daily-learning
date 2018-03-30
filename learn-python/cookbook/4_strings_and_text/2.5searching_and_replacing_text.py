#!/usr/bin/python
# -*- coding utf-8 -*-
import re
from calendar import month_abbr

# for simple literal patterns, use the str.replace() method.
text = 'yeah, but no, but yeah, but no, but yeah'
res = text.replace('yeah', 'yep')
print(res)  # yep, but no, but yep, but no, but yep


# for more complicated patterns, use the sub() functions/methods in the re module. To illustrate, suppose
# you want to rewrite dates of the form "11/27/2012" as "2012-11-27"
text = 'Today is 11/27/2012. Pycon starts 3/13/2013'
res = re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
print(res)  # Today is 2012-11-27. Pycon starts 2013-3-13

# if you're going to perform repeated substitutions of the same pattern, consider compiling it first for better
# performance

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
res = datepat.sub(r'\3-\1-\2', text)
print(res)  # Today is 2012-11-27. Pycon starts 2013-3-13

# for more complicated substitutions, it's possible to specify a substitution callback function instead

def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {} '.format(m.group(2), mon_name, m.group(3))

res = datepat.sub(change_date, text)
print(res)  # Today is 27Nov2012. Pycon starts 13Mar2013

# if you want to know how many substitutions were made in addition to getting the replacement text,
# use re.subn() instead

newtext, n = datepat.subn(r'\3-\1-\2', text)
print(newtext)