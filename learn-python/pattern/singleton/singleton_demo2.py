#!/usr/bin/ python3
# -*- coding: utf-8 -*-


class Singleton(type):
    def __init__(self, *args, **kwargs):
        print("__init__")
        self.__instance = None
        super(Singleton, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        print("__call__")
        print(self)
        print(type(super()))
        print(super(Singleton, self))
        print(super(Singleton, self).__call__(*args, **kwargs))
        if self.__instance is None:
            self.__instance = super(Singleton, self)
        return self.__instance


class Foo(metaclass=Singleton):
    a = 1


foo1 = Foo()
foo2 = Foo()
print(id(foo1), id(foo2))
print (Foo.__dict__ )  #_Singleton__instance': <__main__.Foo object at 0x100c52f10> 存在一个私有属性来保存属性，而不会污染Foo类（其实还是会污染，只是无法直接通过__instance属性访问）
