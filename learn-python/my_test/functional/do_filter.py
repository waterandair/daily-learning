#!/usr/bin/python
# -*- coding utf-8 -*-


def is_odd(n):
    return n % 2 == 1


L = range(100)
print(list(filter(is_odd, L)))


def not_empty(s):
    # strip() 去首位字符，默认去空格
    return s and s.strip()


print(list(filter(not_empty, ['a', 'b', None, '  '])))

