#!/usr/bin/python3
# -*- coding utf-8 -*-
import re


print('test: 010-12345')
m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
print(m.group(1), m.group(2))
