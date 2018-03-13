#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
on the surface, defining a function with optional arguments is easy - simply assign values in the definition and make
sure that default arguments appear last
"""
def spam(a, b=2):
    print(a, b)


"""
If the default value is supposed to be a mutable container, such as a list, set, or dictionary,
use None as the default and write code like this:
"""
def spam(a, b=None):
    if b is None:
        b = []


"""
If instead of providing a default value, you want to write code that merely tests whether an optional argument
was given an interesting value or not, use this idiom
"""
_no_value = object()   # this is very clever operation

def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')



"""!
defining functions with default arguments is easy, but there is a bit more to it than meets the eye

First, the values assigned as a default are bound only once at the time of function definition
For example
"""
x = 24
def spam(a, b=x):
    print(a, b)

spam(1)  # 1 24
x = 2
spam(1)  # 1 24


"""
Second, the values assigned as defaults should always be immutable objects, such as None, True, False, numbers, or 
strings. 
Specifically, never write code like this:
"""
def spam(a, b=[]):  # NO !!!
    pass

"""
If you do this, you can run into all sorts of trouble if the default value ever escapes the function and gets modified.
Such changes will permanently alter the default value across future function calls
"""
def spam(a, b=[]):
    # print(b)
    return b

x = spam(1)
print(x)  # []

x.append(99)
x.append('Yow!')
print(x)  # [99, 'Yow!']

print(spam(1))  # [99, 'Yow!']  Modified list gets returned
"""
To avoid this, it's better to assign None as a default and add a check inside the function for it
"""


"""
The use of the "is" operator when testing for None is a critical part of this  recipe.
The problem here is that although None evaluates to False, many other objects:
(e.g. zero-length strings, lists, tuples, dicts, etc) do as well.
Thus, the test just shown would falsely treat certain inputs as missing
Sometimes people make this mistake:
"""
def spam(a, b=None):
    if not b:           # NO !!!  use 'b' is 'None' instead
        b = []
    pass



