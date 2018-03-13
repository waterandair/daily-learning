#!/usr/bin/python
# -*- coding utf-8 -*-


class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        """是一个对象可以被调用（Callable）"""
        print("my name is %s" % self.name)


Student('kobe')()

"""更多的时候，我们需要判断一个对象是否能被调用，能被调用的对象就是一个Callable对象"""

