#!/usr/bin/python
# -*- coding utf-8 -*-


from operator import itemgetter

L = ['bob', 'about', 'Zoo', 'Credit']

print(sorted(L))  # ['Credit', 'Zoo', 'about', 'bob']
print(sorted(L, key=str.lower))  # ['about', 'bob', 'Credit', 'Zoo']


students = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
print(sorted(students, key=itemgetter(0)))
print(sorted(students, key=lambda x: x[1]))
print(sorted(students, key=itemgetter(0), reverse=True))

