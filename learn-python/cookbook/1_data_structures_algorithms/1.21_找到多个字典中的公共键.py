#!/usr/bin/python3
# -*- coding utf-8 -*-
import random
from functools import reduce

s1 = {x: random.randint(1, 4) for x in random.sample("abcdefg", random.randint(3, 6))}
s2 = {x: random.randint(1, 4) for x in random.sample("abcdefg", random.randint(3, 6))}
s3 = {x: random.randint(1, 4) for x in random.sample("abcdefg", random.randint(3, 6))}
res = reduce(lambda x, y: x & y, map(dict.keys, [s1, s2, s3]))

print(res)







