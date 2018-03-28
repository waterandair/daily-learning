#!/usr/bin/python
# -*- coding utf-8 -*-

# To format a single number for output, use the built-in format() function.
x = 1234.56789
res = format(x, '0.2f')
print(res)  # 1234.57

# right justified in 10 chars, one-digit accuracy
res = format(x, '>10.1f')
print(res)  # '    1234.6'

# left justified
res = format(x, '<10.1f')
print(res)  # '1234.6    '

# centered
res = format(x, '^10.1f')
print(res)  # '  1234.6  '

# inclusion of thousands separator
res = format(x, ',')
print(res)  # 1,234.56789

res = format(x, '0,.1f')
print(res)  # 1,234.6

# If you want to use exponential notation, change the f on an e or E, depending on the case you want used for the
# exponential specifier.
res = format(x, 'e')
print(res)  # 1.234568e+03

res = format(x, '0.2E')
print(res)  # 1.23E+03