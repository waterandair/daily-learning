#!/usr/bin/python
# -*- coding utf-8 -*-
from collections import defaultdict

# if you want to map keys to multiple values, you need to store the multiple values in another container such as a list
# or set
# use a list if you want to preserve the insertion order of the items.use a set if you want to eliminate
# duplicates(and don't care about the order)
d = {
    'a': [1, 2, 3],
    'b': [4, 5]
}

e = {
    'a': {1, 2, 3},
    'b': {4, 5}
}

# you can use defaultdict in the collections to construct such dictionaries easily


d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)

print(d)  # defaultdict(<type 'list'>, {'a': [1, 2], 'b': [4]})

d = defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['a'].add(4)

print(d) # defaultdict(<type 'set'>, {'a': set([1, 2, 4])})

