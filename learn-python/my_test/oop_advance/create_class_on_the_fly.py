#!/usr/bin/python
# -*- coding utf-8 -*-


def fn(self, name='world'):
    print('Hello, %s.' % name)


Hello = type('Hello', (object,), dict(hello=fn))

h = Hello()

print('call h.Hello():')
h.hello()
print('type(Hello):', type(Hello))
print('type(h):', type(h))