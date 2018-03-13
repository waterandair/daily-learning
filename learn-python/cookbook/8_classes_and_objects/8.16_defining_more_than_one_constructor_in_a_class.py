#!/usr/bin/python3
# -*- coding utf-8 -*-
import time
"""
To define a class with more than one constructor, you should use a "class method"
"""
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # Alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)


a = Date(2012, 12, 21)  # Primary
b = Date.today()  # Alternate
