#!/usr/bin/python3
# -*- coding utf-8 -*-
from pyspark import SparkContext

sc = SparkContext("local")

x = sc.parallelize([("a", 1), ("b", 4)])
y = sc.parallelize([("a", 2), ("a", 3), ("c", 5)])

print("join:".rjust(15), sorted(x.join(y).collect()))
print("leftOuterJoin:".rjust(15), sorted(x.leftOuterJoin(y).collect()))
print("rightOuterJoin:".rjust(15), sorted(x.rightOuterJoin(y).collect()))
print("fullOuterJoin:".rjust(15), sorted(x.fullOuterJoin(y).collect()))
