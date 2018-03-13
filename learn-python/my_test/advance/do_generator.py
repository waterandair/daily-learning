#!/usr/bin/python
# -*- coding utf-8 -*-


# 生成器 generator
s = (x * x for x in range(5))
print(s)

for x in s:
    print(x)


# 斐波那契数列
def fib(num):
    n, a, b = 0, 0, 1
    while n < num:
        yield b
        a, b = b, a+b
        n += 1
    return 'done'


f = fib(10)
print(f)

for x in f:
    print(x)

g = fib(5)

while 1:
    try:
        x = next(g)
        print('g:', x)
    except StopIteration as e:
        print('generator return value:', e.value)
        break
