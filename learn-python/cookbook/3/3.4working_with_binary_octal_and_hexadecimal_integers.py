#!/usr/bin/python
# -*- coding utf-8 -*-
import os

# To convert an integer into a binary,octal,or hexadecimal text string,use the bin(),oct(),or hex() functions
x = 1234
print(bin(x))  # 0b10011010010

print(oct(x))  # 02322

print(hex(x))  # 0x4d2

# Alternatively, you can use the format() function if you don't want the 0b, 0o, or 0x prefixes to apper
print(format(x, 'b'))  # 10011010010

print(format(x, 'o'))  # 2322

print(format(x, 'x'))  # 4d2

# Integers are signed, so if you are working with negative numbers, the output will also include a sign
x = -1234
print(format(x, 'b'))  # -10011010010
print(format(x, 'x'))  # -4d2


print(int('4d2', 16))  # 1234
print(int('10011010010', 2))  # 1234


"""
Finally, there is one caution for programmers who use octal.The Python syntax for specifying octal values is slightly
different than many other languages.
Make sure you prefix the octal value with 0o
"""
os.chmod('./3.1rounding_numerical_values.py', 0o755)