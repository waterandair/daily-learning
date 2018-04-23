#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 第二种方法: 继承 type 类

class UpperAttrMetaClass(type):
    # __new__ 是在 __init__之前被调用的特殊方法
    # __new__ 是用来创建并返回对象的方法
    # __init__ 只用来传递参数初始化给对象
    def __new__(cls, future_class_name, future_class_parent, future_class_attr):
        print(future_class_name, future_class_parent, future_class_attr)
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith("__"))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        # return type(future_class_name, future_class_parent, uppercase_attr)
        # return type.__new__(future_class_name, future_class_name, future_class_parent, uppercase_attr)
        return super(UpperAttrMetaClass, cls).__new__(cls, future_class_name, future_class_parent, uppercase_attr)


class Bar(metaclass=UpperAttrMetaClass):
    foo = "foo"


print(hasattr(Bar, "FOO"))


# 第三种方法: 定义一个元类, 实现 __call__() 方法
# 单例模式
class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Spam(metaclass=Singleton):
    def __init__(self):
        print('Creating Spam')


a = Spam()