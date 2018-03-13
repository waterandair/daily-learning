#!/usr/bin/python
# -*- coding utf-8 -*-


class Student(object):
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        """注意使用 @property 装饰器要给属性前面加一个下划线"""
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100')
        self._score = value

    @property
    def phone(self):
        # 使用@property装饰器时会生成一个 phone.setter 装饰器，如果不是使用该装饰器，phone 属性就是一个只读属性
        return '110'


s = Student()
s.score = 90
print('s.score = ', s.score)
# s.score = 101  # ValueError: score must between 0 ~ 100

print('s.phone =', s.phone)
# s.phone = '119'  AttributeError: can't set attribute


