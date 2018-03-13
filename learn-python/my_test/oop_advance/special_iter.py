#!/usr/bin/python
# -*- coding utf-8 -*-


class Fib(object):
    """斐波那契数列"""
    def __init__(self):
        self.a, self.b = 0, 1  # 初始化两个计数器

    def __iter__(self):
        """__iter__(self)返回一个迭代对象，然后，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环。"""
        return self  # 实例本身就是迭代对象,故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 100:
            raise StopIteration()
        return self.a


for n in Fib():
    print(n)
