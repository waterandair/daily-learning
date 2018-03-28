#!/usr/bin/python3
# -*- coding utf-8 -*-

# use the built-in reversed() function
a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)

# 4
# 3_num_date_time
# 2
# 1

"""
Reversed iteration only works if the object in question has a size that can be determined or if the object implements
the object implements a __reversed__() special method.
If neither of these can be satisfied, you'll have to convert the object into a list first
"""
with open('./test.txt') as f:
    for line in reversed(list(f)):
        print(line, end='|')

"""!!!
Be aware that turning an iterable into a list as shown could consume a lot of memory if it's large
"""

"""!!!
Defining a reversed iterator makes the code much more efficient, as it's no longer necessary to pull the data into a 
list and iterable in reverse on the list
"""