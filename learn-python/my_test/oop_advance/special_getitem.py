#!/usr/bin/python
# -*- coding utf-8 -*-


class Fib(object):

    def __getitem__(self, item):
        """使实例表现的像 list 一样可以用下标取出"""
        if isinstance(item, int):
            a, b = 1, 1
            for x in range(item):
                a, b = b, a + b
            return a

        """判断传入的是否是切片对象"""
        if isinstance(item, slice):
            start = item.start
            stop = item.stop

            if start is None:
                start = 0
            a, b = 1, 1
            l = []
            for x in range(stop):
                if x > start:
                    l.append(a)
                a, b = b, a + b
            return l


f = Fib()

print(f[0])  # 1
print(f[5])  # 8
print(f[100])  # 573147844013817084101
print(f[0:5])  # [1, 2, 3, 5]
print(f[:10])  # [1, 2, 3, 5, 8, 13, 21, 34, 55]
