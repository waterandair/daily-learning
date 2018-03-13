#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
Functions arguments annotations can be a useful way to give programmers hints about how a function is supposed to be
used. For example, consider the following annotated function:
"""
def add(x:int, y:int) -> int:
    return x+y

"""
The python interpreter does not attach any semantic meaning to the attached annotations.They are not type checks, nor do 
they make python behave any differently than it did before.
However, they might give useful hints to others reading the source code about what you had in mind.
Third-party tools and frameworks might also attach semantic meaning to the annotations.
"""
help(add)

"""
Help on function add in module __main__:

add(x:int, y:int) -> int
"""


"""
Function annotations are merely stored in a function's __annotations__ attribute
"""
print(add.__annotations__)  # {'y': <class 'int'>, 'return': <class 'int'>, 'x': <class 'int'>}

