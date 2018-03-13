#!/usr/bin/python3
# -*- coding utf-8 -*-
import html
"""
To write a function that accepts any number of positional arguments, use a * argument
"""


def avg(first, *rest):
    print(type(rest))  # <type 'tuple'>
    return (first + sum(rest)) / (1 + len(rest))

# sample use
print(avg(1, 2))  # 1.5
print(avg(1, 2, 3, 4))  # 2.5

"""
In this example, rest is a tuple of all the extra positional arguments passed.
The code treats it as a sequence in performing subsequent calculations.
To accept any number of keyword arguments, use an argument that starts with **
Here,attrs is a dictionary that holds the passed keyword argument(if any)
"""
def make_element(name, value, **attrs):
    keyvals = [' %s="%s" ' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(name=name, attrs=attr_str, value=html.escape(value))
    return element

# Example
element = make_element('item', 'Albatross', size='large', quantity=6)
print(element)  # <item quantity="6"  size="large" >Albatross</item>

element = make_element('p', '<spam>')
print(element)  # <p>&lt;spam&gt;</p>


"""
If you want a function that can accept both any number of positional and keyword-only arguments, use * and ** together.
With this function, all of the positional arguments are placed into a tuple args, and all of the keyword arguments are 
placed into a dictionary kwargs 
"""
def anyargs(*args, **kwargs):
    print(args)  # A tuple
    print(kwargs)  # A dict



"""
A * argument can only appear as the last positional argument in a function definition.
A ** argument can only appear as the last argument.
A subtle aspect of function definitions is that arguments can still appear after a * argument
"""
def a (x, *args, y):
    pass
def b (x, *args, y, **kwargs):
    pass

