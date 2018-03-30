#!/usr/bin/python
# -*- coding utf-8 -*-
from collections import OrderedDict

d = {
    'a': '1',
    'b': '2',
    'c': '3',
    'd': '4',
}
print(d)  # {'a': '1', 'c': '3', 'b': '2', 'd': '4'} the default is not arranged in the order of insertion

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4

for key in d:
    print(key, d[key])


