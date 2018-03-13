#!/usr/bin/python3
# -*- coding utf-8 -*-
from datetime import date
"""
To customize string formatting, define the __format__() method on a class.
"""
_formats = {
    'ymd': '{d.year}-{d.month}-{d.day}',
    'mdy': '{d.month}/{d.day}/{d.year}',
    'dmy': '{d.day}/{d.month}/{d.year}'
    }

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, format_spec):
        if format_spec == '':
            format_spec = 'ymd'
        fmt = _formats[format_spec]
        return fmt.format(d=self)

"""
Instance of the Date class now support formatting operations such as the following
"""
d = Date(2012, 12, 21)
print(format(d))  # 2012-12_concurrency-21
print(format(d, 'mdy'))  # 12_concurrency/21/2012
print('The date is {:ymd}'.format(d))  # The date is 2012-12_concurrency-21
print('The date is {:mdy}'.format(d))  # The date is 12_concurrency/21/2012


"""
The __format__() method provides a hook into Python's string formatting functionality.It's important to emphasize that 
the interpretation of format codes is entirely up to the class itself.
Thus, the codes can be almost anything at all.
"""
d = date(2012, 12, 21)
print(format(d))  # 2012-12_concurrency-21
print(format(d,'%A, %B %d, %Y'))  # Friday, December 21, 2012
print('The end is {:%d %b %Y}. Goodbye'.format(d))  # The end is 21 Dec 2012. Goodbye

