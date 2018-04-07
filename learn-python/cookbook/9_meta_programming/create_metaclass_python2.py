#!/usr/bin/python
# -*- coding:utf-8 -*-

# 第一种方法(python2 中), 在模块或类中定义 __metaclass__
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    '''返回一个类对象，将属性都转为大写形式'''
    #  选择所有不以'__'开头的属性
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    # 将它们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)

    # 通过'type'来做类对象的创建
    return type(future_class_name, future_class_parents, uppercase_attr)


class Foo(object):
    __metaclass__ = upper_attr
    bar = 'bip'

print(hasattr(Foo, "BAR"))


# 第二种方法: 继承 type 类

class UpperAttrMetaClass(type):
    # __new__ 是在 __init__之前被调用的特殊方法
    # __new__ 是用来创建并返回对象的方法
    # __init__ 只用来传递参数初始化给对象
    def __new__(cls, future_class_name, future_class_parent, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith("__"))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        # return type(future_class_name, future_class_parent, uppercase_attr)
        # return type.__new__(future_class_name, future_class_name, future_class_parent, uppercase_attr)
        return super(UpperAttrMetaClass, cls).__new__(cls, future_class_name, future_class_parent, uppercase_attr)


class Bar(metaclass=UpperAttrMetaClass):
    foo = "foo"


bar = Bar()
print(hasattr(bar, "FOO"))
