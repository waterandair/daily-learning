#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
A bare uninitialized instance can be created by directly calling the __new__() method of a class
"""
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


d = Date.__new__(Date)
data = {
    'year': 2012,
    'month': 12,
    'day': 12
}
for key, value in data.items():
    setattr(d, key, value)


"""
 By using setattr() to set the values, your code will be as general purpose as possible.
"""

