#!/usr/bin/python
# -*- coding utf-8 -*-

from collections import Iterable, Iterator


def g():
    yield 1
    yield 2
    yield 3


# 打印出来不是按照写定的顺序输出的
d = {'a': 1, 'b': 2, 'c': 3}

print('Iterable? [1, 2, 3]: ', isinstance([1, 2, 3], Iterable))
print('Iterable? \'abc\' : ', isinstance('abc', Iterable))
print('Iterable? 123 : ', isinstance(123, Iterable))
print('Iterable? g() : ', isinstance(g(), Iterable))
print('Iterable? {\'a\': 1, \'b\': 2, \'c\': 3}', isinstance({'a': 1, 'b': 2, 'c': 3}, Iterable))

print('--------------------------------------')

print('Iterator? [1, 2, 3] : ', isinstance([1, 2, 3], Iterator))
print('Iterator? iter([1, 2, 3])', isinstance(iter([1, 2, 3]), Iterator))
print('Iterator? \'abc\' : ', isinstance('abc', Iterator))
print('Iterator? 123:', isinstance(123, Iterator))
print('Iterator? g():', isinstance(g(), Iterator))
print('Iterator? {\'a\': 1, \'b\': 2, \'c\': 3}:', isinstance(d, Iterator))
print('Iterator? iter({\'a\': 1, \'b\': 2, \'c\': 3}):', isinstance(iter(d), Iterator))

print('for x in [1, 2, 3, 4, 5]')
for x in [1, 2, 3, 4, 5]:
    print(x)

print('for x in iter([1, 2, 3, 4, 5])')
for x in iter([1, 2, 3, 4, 5]):
    print(x)

print("next():")
it = iter([1, 2, 3, 4, 5])
print(next(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))

print('iter key:', d)
for key in d.keys():
    print('key:', key)

print('iter value:', d)
for value in d.values():
    print('values', value)

print('iter item', d)
for k, v in d.items():
    print('key:', k, 'value', v)

# iter list with index
# enumerate 第二个参数可以置顶厨师索引值
print('iter enumerate([\'A\', \'B\', \'C\'])')
for i, value in enumerate(['A', 'B', 'C'], 3):
    print(i, value)


# # 如果要统计文件的行数，可以这样写：
# count = len(open(filepath, 'r').readlines())
# 这种方法简单，但是可能比较慢，当文件比较大时甚至不能工作。
#
# 可以利用enumerate()：
#
# count = 0
# for index, line in enumerate(open(filepath,'r'))：
#     count += 1

print('iter [(1, 1), (2, 4), (3, 9)]:')
for x, y in [(1, 1), (2, 4), (3, 9)]:
    print(x, y)
