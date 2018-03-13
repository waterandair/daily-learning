#!/usr/bin/python3
# -*- coding utf-8 -*-
import re

# the split() method of string objects is really meant for very simple cases, and does not
# allow for multiple delimiters or account for possible whitespace around the delimiters.
# In cases when you need a bit more flexibility, use the re.split() method

line = 'asdf fjdk; afed, fjek,asdf,      foo'
str = re.split(r'[;,\s]\s*', line)
print(str)  # ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# if capture groups are used, then the matched text is alse included in result.

fields = re.split(r'(;|,|\s)\s*', line)
print(fields)  # ['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']

# getting the split characters might be useful in certain contexts.For example, maybe you need
# the split characters later on to reform an output string

values = fields[::2]
delimiters = fields[1::2] + ['']
print(delimiters)  # [' ', ';', ',', ',', ',', '']

line = ''.join(v+d for v, d in zip(values, delimiters))
print(line)  # asdf fjdk;afed,fjek,asdf,foo

# if you don't want the separator characters in the result , but still need to use parentheses to group
# parts of the regular expression pattern, make sure you use a noncapture group, specified as (?:...)

fields = re.split(r'(?:,|;|\s)\s*', line)
print(fields)  # ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
