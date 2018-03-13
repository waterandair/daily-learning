#!/usr/bin/python
# -*- coding utf-8 -*-


from enum import Enum, unique


@unique
class Weekday(Enum):
    Sun = 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6


day1 = Weekday.Mon

print(day1)
print(Weekday.Tue)
print(Weekday['Tue'])
print(Weekday.Tue.value)
print(Weekday.Mon == day1)
print(Weekday.Tue == day1)
print(Weekday(1))

for name, member in Weekday.__members__.items():
    print(name, '=>', member)

print('**********************************')

month = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
Month = Enum('Month', month)

for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)
