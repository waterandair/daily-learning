#!/usr/bin/python3
# -*- coding utf-8 -*-
import sys

"""
Python has no direct support for simply substituting variable values in strings.
However, this feature can be approximated using the format() method of strings.
"""
s = '{name} has {n} messages.'
res = s.format(name='kobe', n=99)
print(res)  # kobe has 99 messages.

"""
Alternatively, if the values to be substituted are truly found in variables, you can use the combination of format_map()
and vars()
"""
name = 'jordan'
n = 98
res = s.format_map(vars())
print(res)  # jordan has 98 messages.

# One subtle feature of vars() is that it also works with instances.
class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n


a = Info('wade', 97)
res = s.format_map(vars(a))
print(res)  # wade has 97 messages.


# One downside of format() and format_map() is that they do not deal gracefully with missing values
# One way to avoid this is to define an alternative dictionary class with a __missing__() method
class Safesub(dict):
    def __missing__(self, key):
        return "{{key}}".format(key=key)


del n
res = s.format_map(Safesub(vars()))
print(res)  # jordan has n messages.


"""
If you find yourself frequently performing these steps in your code, you could hide the variable substitution process 
behind a small utility function that employs a so-called "frame hack"
"""
def sub(text):
    return text.format_map(Safesub(sys._getframe(1).f_locals))


name = 't-mac'
n = 13
res = sub('Hello {name}')
print(res)  # Hello t-mac

res = sub('You have {n} messages.')
print(res)  # You have 13 messages.

res = sub('Your favorite color is {color}')
print(res)  # Your favorite color is {color}
