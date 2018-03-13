#!/usr/bin/python
# -*- coding utf-8 -*-
import itertools


def count(n):
    while True:
        yield n
        n += 1
