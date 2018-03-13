#!/usr/bin/python
# -*- coding utf-8 -*-

from io import BytesIO

# 内存中读写二进制数据

f = BytesIO()
f.write(b'hello')
f.write(b' ')
f.write(b'world')
print(f.getvalue())

data = '人闲桂花落，夜静春山空。月出惊山鸟，时鸣春涧中。'.encode('utf-8')
f = BytesIO(data)
print(f.read())