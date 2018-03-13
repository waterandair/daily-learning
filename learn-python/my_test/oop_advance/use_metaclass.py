#!/usr/bin/python
# -*- coding utf-8 -*-

# metaclass 是创建类，所以必须从 'type' 类型派生


class ListMetaclass(type):
    def __new__(cls, name, bases, attrs, *args, **kwargs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs, *args, **kwargs)


# 使用 ListMetaclass 定制类
class List(list, metaclass=ListMetaclass):
    pass


L = List()
L.add(1)
L.add(2)
L.add(3)
L.add('END')

print(L)
