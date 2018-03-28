#!/usr/bin/python3
# -*- coding utf-8 -*-

class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)


"""
The __repr__() method returns the code representation fo an instance, and is usually the text you would type to 
re-create the instance.
The built-in repr() function returns this text, as does the interactive interpreter when inspecting values.

The __str__ method converts the instance to a string, and is the output produced by the str() and print() function
"""
p = Pair(3, 4)
p
# Pair(3_num_date_time, 4)  __repr__() output
print(p)
# (3_num_date_time, 4)  __str__() output
