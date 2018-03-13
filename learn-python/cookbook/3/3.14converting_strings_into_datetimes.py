#!/usr/bin/python
# -*- coding utf-8 -*-
from datetime import datetime
text = '2017-11-16'
y = datetime.strptime(text, "%Y-%m-%d")
print(type(y))  # <type 'datetime.datetime'>
print(y)  # 2017-11-16 00:00:00

""" !!!
it's worth nothing that the performance of strptime() is often much worse than you might expect, due to
the fact that it's written in pure Python and it has to deal with all sorts of system locale settings.

If you are parsing a lot of dates in your code and you know the precise format, you will probably get much 
better performance by cooking up a custom solution instead.

For example, if you knew that the dates were of the form "YYYY-MM-DD", you could write a function like this 
"""


def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))


"""
When tested, this function runs over seven!!! times faster than datetime.strptime().
"""