#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
To call a method in a parent (or superclass), use the super() function
"""

class A :
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super(B, self).spam()  # Call parent spam()

b = B()
b.spam()
"""
B.spam
A.spam
"""

"""
A very common use of super() is in the handling of the init() method to make sure that parents are properly initialized
"""

class A:
    def __init__(self):
        self.x = 0

class B(A):
    def __init__(self):
        super(B, self).__init__()
        self.y = 1

b = B()
print(b.x, b.y)  # 0 1

"""
Another common use of super() is in code that overrides any of Python's special methods
"""
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, item):
        return getattr(self._obj, item)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super(Proxy, self).__setattr__(key, value)
        else:
            setattr(self._obj, key, value)


class D():
    def spam(self):
        print('D')
    pass

class E:
    def spam(self):
        print('E')

class F:
    def spam(self):
        print('F')

class G(D):
    pass
    # def spam(self):
    #     print('G')

class H(G, E):
    def spam(self):
        E.spam(self)
    pass

h = H()  # [<class '__main__.H'>, <class '__main__.G'>, <class '__main__.D'>, <class '__main__.E'>, <class 'object'>]
h.spam()
print(H.mro())