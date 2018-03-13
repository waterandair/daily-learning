#!/usr/bin/python
# -*- coding utf-8 -*-


def lazy_sum(*args):
    def sums():
        ax = 0
        for n in args:
            ax += n
        return ax
    return sums


f = lazy_sum(1, 2, 3, 4, 5, 6)
print(f)
print(f())


def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i * i
        fs.append(f)
    return fs


f1, f2, f3 = count()

print(f1())
print(f2())
print(f3())
