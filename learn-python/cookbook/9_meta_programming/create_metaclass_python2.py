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
