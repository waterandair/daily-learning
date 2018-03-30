#!/usr/bin/python3
# -*- coding utf-8 -*-

res = round(1.23, 1)
print(res)  # 1.2

res = round(1.27, 1)
print(res)  # 1.3

res = round(-1.27, 1)
print(res)  # -1.3

res = round(1.25361, 3)
print(res)  # 1.254

res = round(1.5)
print(res)  # 2

res = round(2.5)
print(res)  # in python2.7 is '3' but is '2' in python3

a = 1627731
res = round(a, -1)  # 1627730
print(res)

res = round(a, -2)  # 1627700
print(res)

res = round(a, -3)  # 1628000
print(res)


# Don't confuse rounding with formatting a value for output. If your goal is simply to output a numerical value with a
# certain number of decimal places, you don't typically need to use round()
# Instead, just specify the desired precision when formatting.

x = 1.23456
print(format(x, '0.2f'))  # 1.23
print(format(x, '0.3f'))  # 1.235
print('value is {:0.3f}'.format(x))  # value is 1.235

