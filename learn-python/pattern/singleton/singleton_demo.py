#!/usr/bin/ python3
# -*- coding: utf-8 -*-


class Singleton1(object):
    """
    1. 使用 __new__方法
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance


class Test1(Singleton1):
    a = 1


a, b = Test1(), Test1()
print(id(a), id(b))


class Singleton2(object):
    """
    2. 使用共享属性
    共享属性;所谓单例就是所有引用(实例、对象)拥有相同的状态(属性)和行为(方法)
    同一个类的所有实例天然拥有相同的行为(方法),
    只需要保证同一个类的所有实例具有相同的状态(属性)即可
    所有实例共享属性的最简单最直接的方法就是__dict__属性指向(引用)同一个字典(dict)
    """

    _state = {}

    def __new__(cls, *args, **kwargs):
        ob = super().__new__(cls, *args, **kwargs)
        ob.__dict__ = cls._state
        return ob


class Test2(Singleton2):
    a = 1


a, b = Test2(), Test2()
print(a.__dict__)
print(id(a.__dict__), id(b.__dict__))


class Singleton3(type):
    """
    3. 元类方法
    """
    def __init__(cls, name, bases, dict):
        super(Singleton3, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton3, cls).__call__(*args, **kw)   # 这句你怎么理解?
        return cls._instance


class MyClass3(metaclass=Singleton3):
    a = 1


one = MyClass3()
two = MyClass3()

print(id(one), id(two))


def singleton(cls, *args, **kw):
    """
    4. 装饰器方法
    """
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class Test4(object):
    a = 1


one = Test4
two = Test4
print(id(one), id(two))