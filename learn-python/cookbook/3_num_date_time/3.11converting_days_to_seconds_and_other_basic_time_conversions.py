#!/usr/bin/python3
# -*- coding utf-8 -*-
from datetime import timedelta
from datetime import datetime
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a+b
print(c.days)  # 2
print(c.seconds)  # 37800
print(c.seconds/3600)  # 10.5   (in python2.7 is '10')
print(c.total_seconds() / 3600)  # 58.5

"""
If you need to represent specific dates and times, create datetime instances and use the standard mathematical
operations to manipulate them
"""
a = datetime(2012, 9, 23)
print(a + timedelta(days=10))  # 2012-10-03 00:00:00

b = datetime(2012, 12, 21)
d = b - a
print(d)  # 89 days, 0:00:00
print(d.days)  # 89

now = datetime.today()
print(now)  # 2017-11-16 17:54:51.950084
print(now + timedelta(minutes=10))  # 2017-11-16 18:05:30.434214

# when making calculations, it should be noted that datetime is aware of leap years.
a = datetime(2012, 3, 1)
b = datetime(2012, 2, 28)
print(a-b)  # 2 days, 0:00:00

c = datetime(2013, 3, 1)
d = datetime(2013, 2, 28)
print(c - d)  # 1 day, 0:00:00