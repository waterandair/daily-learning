#!/usr/bin/python3
# -*- coding utf-8 -*-


class LoggedMappingMixin:
    """
    Add logging to get/set/delete operations for debugging
    """
    __slots__ = ()  # 混入类都没有实例变量，因为直接实例化混入类没有任何意义

    def __getitem__(self, item):
        print("getting " + str(item))
        return super(LoggedMappingMixin, self).__getitem__(item)

    def __setitem__(self, key, value):
        print('setting {} = {}'.format(key, value))
        return super(LoggedMappingMixin, self).__setitem__(key, value)

    def __delitem__(self, key):
        print('deleting ' + str(key))
        return super(LoggedMappingMixin, self).__delitem__(key)
    
    
class SetOnceMappingMixin:
    """
    Only allow a key to be set once
    """
    __slots__ = ()
    
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + 'already set')
        return super(SetOnceMappingMixin, self).__setitem__(key, value)


class StringKeysMappingMixin:
    """
    Restrict keys to strings only
    """
    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('keys must be strings')
        return super(StringKeysMappingMixin, self).__setitem__(key, value)


"""
These classes, by themselves, are useless. In fact, if you instantiate any one of them, it does nothing useful at all,
Instead, they are supposed to be mixed with other mapping classes through multiple inheritance
"""
class LoggedDict(LoggedMappingMixin, dict):
    pass


d = LoggedDict()
d['x'] = 24  # setting x = 24
d['x']  # getting x
del d['x']  # deleting x


"""
An alternative implementation of mixins involves the use of class decorators.
"""
def LoggedMapping(cls):
    cls_getitem = cls.__getitem__
    cls_setitem = cls.__setitem__
    cls_deltiem = cls.__delitem__

    def __getitem__(self, item):
        print('getting ' + str(item))
        return cls_getitem(self, item)

    def __setitem__(self, key, value):
        print('setting {} = {}'.format(key, value))
        return cls_setitem(self, key, value)

    def __delitem__(self, key):
        print('deleting ' + str(key))
        return cls_deltiem(self, key)

    cls.__getitem__ = __getitem__
    cls.__setitem__ = __setitem__
    cls.__delitem__ = __delitem__

    return cls

@LoggedMapping
class LoggedDict(dict):
    pass