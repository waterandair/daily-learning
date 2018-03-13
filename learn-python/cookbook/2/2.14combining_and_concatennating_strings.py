#!/usr/bin/python3
# -*- coding utf-8 -*-

# If the strings you wish to combine are found in a sequence or iterable, the faster way to combine them is to use the
# join() method

parts = ['Is', 'Chicago', 'Not', 'Chicago?']
res = ' '.join(parts)
print(res)  # Is Chicago Not Chicago?

res = ','.join(parts)
print(res)  # Is,Chicago,Not,Chicago?

# If you only combining a few strings, using + usually works well enough

# If you're trying to combine string literals together in source code, you can simply place them adjacent to each
# other with no + operator. For example:

a = 'Hello' 'world'
print(a)  # 'Helloworld'

# !!!
# The most important thing to know is that using the + operator to join a lot of strings together is grossly inefficient
# due to the memory copies and garbage collection that occurs. In particular,you never want to write code that joins
# strings like this:
s = ''
for p in parts:
    s += p
# This runs quite a bit slower than using the join() method, mainly because each += operation creates a new string
# object.You're better off just collection all of parts first and then joining them together an the end


# One related (and pretty neat) trick is the conversion of data to strings and concatenation at the same time using a
# generation expression
data = ['ACME', 50, 91.1]
res = ','.join(str(d) for d in data)
print(res)  # ACME,50,91.1

# Also be on the lookout for unnecessary string concatenations.Sometimes programmers get carried away with concatenation
# when it's really not technically necessary.
a, b, c = 'a', 'b', 'c'
print(a + ':' + b + ':' + c)  # Ugly
print(':'.join([a, b, c]))  # Still Ugly
print(a, b, c, sep=':')  # Better


# Mixing I/O operations and string concatenation is something that might require study in your application
# Version 1
# f.write(chunk1 + chunk2)

# Version 2
# f.write(chunk1)
# f.write(chunk2)

# If the two strings are small, the first version might offer much better performance due to the inherent expense of
# carrying out an I/O system call.
'''
    on the other hand, if the two strings are large, the second version may be more efficient, since it avoid making a
large temporary result and copying large blocks of memory around.Again, it must be stressed that this is something you 
would have to study in relation to your own data in order to determine which performs best.
'''


'''
Last, but not least, if you're writing code that is building output from lots of small strings, you might consider
writing that code as a generator function, using yield to emit fragments.
For example
'''


def sample():
    yield 'Is'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'


'''
The interesting thing about this approach is that it makes no assumption about how the fragments are to be assumption 
together.
'''
# You could simply join the fragments using join()
text = ''.join(sample())
print(text)  # IsChicagoNotChicago?

# Or you could redirect the fragments to I/O
with open('test2.txt', 'w') as f:
    for part in sample():
        f.write(part)

# Or you could come up with some kind of hybrid scheme that's smart about combining I/O operations
def combine(source, maxsize):
    parts = []
    size = 0
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield ''.join(parts)
            parts = []
            size = 0
    yield ''.join(parts)


with open('text3.txt', 'w') as f:
    for part in combine(sample(), 5):
        f.write(part+'\n')

"""
The key point is that the original generator function doesn't have to know the precise details. It just yields the parts
"""