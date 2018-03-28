#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
Use the sep and end keyword arguments to print() to change the output as you wish
"""
print('hello', 50, 91.5)  # hello 50 91.5

print('hello', 50, 91.5, sep=',')  # hello,50,91.5

print('hello', 50, 91.5, sep=',', end='!!\n')  # hello,50,91.5!!


"""
Use of the end argument is also how you suppress the output of newlines in output
"""
for i in range(5):
    print(i)

"""
0
1
2
3_num_date_time
4
"""

for i in range(5):
    print(i, end='|')

# 0|1|2|3_num_date_time|4|


"""
sometimes you'll see programmers using str.join() to accomplish the same thing.
"""
print(','.join(('hello', '50', '95.2')))  # hello,50,95.2
"""
But, the problem with str.join() is that it only works with strings
"""
# TypeError: sequence item 1: expected str instance, int found
# print(','.join(('hello', 50, 95.2)))

row = ('ACME', 50, 91.5)
print(*row, sep='|')  # ACME|50|91.5