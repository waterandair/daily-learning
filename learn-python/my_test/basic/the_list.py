#!/usr/bin/python
# -*- coding utf-8 -*-
classmates = [
    'kobe',
    'wade',
    't-mac'
]
print('''
    classmates = %s
    len(classmates) = %d
    classmates[0] = %s
    classmates[1] = %s
    classmates[2] = %s
    classmates[-1] = %s
    classmates[-2] = %s
''' % (classmates, len(classmates), classmates[0], classmates[1],
       classmates[2], classmates[-1], classmates[-2]))
classmates.pop()
print(classmates)
