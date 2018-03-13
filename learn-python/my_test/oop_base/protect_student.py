#!/usr/bin/python
# -*- coding utf-8 -*-


class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score

    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')

    def get_grade(self):
        if self.__score >= 90:
            return 'A'
        elif self.__score >= 80:
            return 'B'
        else:
            return 'C'


kobe = Student('kobe', 90)

# print(kobe.name)  # AttributeError: 'Student' object has no attribute 'name'
print(kobe.get_name())
# print(kobe.__name)  # AttributeError: 'Student' object has no attribute '__name'
print(kobe._Student__name)  # python 的私有属性不是强制的，按照约定，是“_类名__属性名”
