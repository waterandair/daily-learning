#!/usr/bin/python
# -*- coding utf-8 -*-


class Student(object):

    def __init__(self):
        self.name = 'kobe'

    def __getattr__(self, item):
        """当调用不存在的属性或方法时程序会走到 __getattr__ 中"""
        return type(item)


s = Student()
print(s.name)
print(s.score)
print(s.age())
# AttributeError: 'Student' object has no attribute 'grade'
print(s.grade)