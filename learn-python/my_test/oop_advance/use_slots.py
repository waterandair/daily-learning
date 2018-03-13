#!/usr/bin/python
# -*- coding utf-8 -*-


class Student(object):
    __slots__ = ('name', 'age')  # 用tuple定义允许绑定的属性名称


class GraduateStudent(Student):
    # 子类如果不设置__slots__，就不会继承父类的__slots__，如果子类设置了__slots__，子类的__slots__就是父类__slots__和子类__slots__的并集
    __slots__ = ()


s = Student()
s.name = 'kobe'
s.age = 40

# AttributeError: 'Student' object has no attribute 'score'
# s.score = 81

g = GraduateStudent()
g.score = 99  # AttributeError: 'GraduateStudent' object has no attribute 'score'
print('g.score =', g.score)

