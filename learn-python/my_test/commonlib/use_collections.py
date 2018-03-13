#!/usr/bin/python3
# -*- coding utf-8 -*-

# namedtuple是一个函数，它用来创建一个自定义的tuple对象，
# 并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。
from collections import namedtuple

# 使用list存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，
# 因为list是线性存储，数据量大的时候，插入和删除效率很低。
# deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈：
from collections import deque

# 使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用 defaultdict
from collections import defaultdict

# 保持Key的顺序
from collections import OrderedDict

# 简单的计数器
from collections import Counter

Point = namedtuple('Point', ['x', 'y'])
point = Point(1, 2)
print('Point:', point.x, point.y)

q = deque(['a', 'b', 'c'])
q.append('d')
q.popleft()
q.appendleft('z')
print('deque:', q)

dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
print('dd[\'key1\'] =', dd['key1'])
print('dd[\'key2\'] =', dd['key2'])


#OrderedDict 可以实现一个 FIFO（先进先出） 的 dict， 当容量超出限制时，先删除最早添加的key
class LastUpdatedOrderedDict(OrderedDict):
    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()
        self.__capacity = capacity

    def __setitem__(self, key, value):
        contansKey = 1 if key in self else 0
        if len(self) - contansKey >= self.__capacity:
            # The popitem() method for ordered dictionaries returns and removes a (key, value) pair.
            # The pairs are returned in LIFO order if last is true or FIFO order if false.
            last = self.popitem(last=False)
            print ('remove:', last)
        if contansKey:
            del self[key]
            print ('set:', (key, value))
        else:
            print ('add:', (key, value))
        OrderedDict.__setitem__(self, key, value)


fifo = LastUpdatedOrderedDict(3)
fifo.setdefault('a', 'a')
fifo.setdefault('b', 'b')
fifo.setdefault('c', 'c')
fifo.setdefault('d', 'd')
print (list(fifo))

c = Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1
print(c)


