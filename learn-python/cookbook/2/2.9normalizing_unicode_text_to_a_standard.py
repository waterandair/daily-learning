#!/usr/bin/python3
# -*- coding utf-8 -*-
import unicodedata

# In Unicode, certain characters can be represented by more than one valid sequence of code points.
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'

print(s1)  # Spicy Jalapeño
print(s2)  # Spicy Jalapeño

print(s1 == s2)  # False
print(len(s1))  # 14
print(len(s2))  # 15


# Having multiple representations is a problem for programs that compare strings.In order to fix this,
# you should first normalize the text into a standard representation using the unicodedata module
t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
print(t1 == t2)  # True

t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)
print(t3 == t4)  # True

print(ascii(t1))  # 'Spicy Jalape\xf1o'
print(ascii(t3))  # 'Spicy Jalapen\u0303o'
