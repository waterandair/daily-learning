#!/usr/bin/python
# -*- coding utf-8 -*-
from collections import Iterator
from collections import Iterable

"""
You have built a custom container object that internally holds a list, or some other iterable.
You would like to make iteration work with your new container.

Typically, all you need to do is define an __iter__() method that delegates iteration to the internally
held container.
"""
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return "Node({})".format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)


if __name__ == '__main__':
    root = Node(0)

    child1 = Node(1)
    child2 = Node(2)

    root.add_child(child1)
    root.add_child(child2)

    for ch in root:
        print(ch)

    print(isinstance(root, Iterable))  # True
    print(isinstance(root, Iterator))  # False
