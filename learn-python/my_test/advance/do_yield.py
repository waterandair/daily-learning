#!/usr/bin/python
# -*- coding utf-8 -*-


def each_ascii(s):
    for ch in s:
        # ord(ch) 返回对应的 ASCII 数值，或者 Unicode 数值
        yield ord(ch)
    return '%s chars' % len(s)


def yield_from(s):
    r = yield from each_ascii(s)
    print(r)


def main():
    # for x in each_ascii('abc'):
    #     print(x)

    # it = each_ascii('xyz')
    # try:
    #     while True:
    #         print(next(it))
    # except StopIteration as s:
    #     print(s.value)

    # using yield from in main() will change main() from function to generator:
    # r = yield from each_ascii('hello')

    yield from each_ascii('hello')


for x in main():
    print(x)
