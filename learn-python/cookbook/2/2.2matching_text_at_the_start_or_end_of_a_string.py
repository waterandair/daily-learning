#!/usr/bin/python3
# -*- coding utf-8 -*-
import os
# you need to check the start or end of a string for specific text patterns, such as filename extensions
# URL schemes, and so on.

# A simple way to check the begining or end of a string is to use the str.startswith() or str.endswith() methods.

filename = 'spam.txt'
print(filename.endswith('.txt'))  # True
print(filename.startswith('.txt'))  # False

url = "http://www.python.org"
print(url.startswith('http:'))  # True

# if you need to check against multiple choices, simply provide a tuple of possibilities to startswith() or endswith()
filenames = os.listdir('.')
print(filenames)

print([name for name in filenames if name.endswith(('.c', '.h', '.py'))])
# ['2.2matching_text_at_the_start_or_end_of_a_string.py', '2.1splitting_strings_on_any_of_multiple_delimiters.py']

print(any(name.endswith('.py') for name in filenames))  # True

# oddly, this is on part of python where a tuple is actually required as input. If you happen to have the choices
# specified in a list or set , just make sure you convert them using tuple() first

choices = ['http:', 'ftp:']
url = 'http://www.python.org'
# url.startswith(choices)  # TypeError: startswith first arg must be str or a tuple of str, not list
