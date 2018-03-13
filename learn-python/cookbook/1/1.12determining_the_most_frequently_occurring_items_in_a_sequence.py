#!/usr/bin/python
# -*- coding utf-8 -*-
from collections import Counter

words = [
   'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
   'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
   'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
   'my', 'eyes', "you're", 'under'
]

word_counts = Counter(words)
print(word_counts)
# Counter({'eyes': 8, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2, "you're": 1,
# "don't": 1, 'under': 1, 'not': 1})
top_three = word_counts.most_common(3)
print(top_three)  # [('eyes', 8), ('the', 5), ('look', 4)]

print(word_counts['eyes'])
print(word_counts['not'])

# a little-know feature of Counter instances is that they can be easily combined using
# various mathematical operations
morewords = ['why', 'are', 'you', 'not', 'looking', 'in', 'my', 'eyes']
a = Counter(words)
b = Counter(morewords)

c = a + b
print(c)
# Counter({'eyes': 9, 'the': 5, 'look': 4, 'my': 4, 'into': 3, 'not': 2, 'around': 2,
# "you're": 1, "don't": 1, 'in': 1, 'why': 1, 'looking': 1, 'are': 1, 'under': 1, 'you': 1})

d = a - b
print(d)
# Counter({'eyes': 7, 'the': 5, 'look': 4, 'into': 3, 'my': 2, 'around': 2, "you're": 1,
# "don't": 1, 'under': 1})
