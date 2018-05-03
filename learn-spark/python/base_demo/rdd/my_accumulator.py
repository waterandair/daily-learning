#!/usr/bin/python3
# -*- coding utf-8 -*-
from pyspark import SparkContext
from pyspark import AccumulatorParam


class MyAccum(AccumulatorParam):

    def zero(self, value):
        return {"a": 0, "b": 0, "c": 0, "d": 0}

    def addInPlace(self, value1, value2):
        if value1 == "":
            return value2
        if isinstance(value2, dict):
            # rdd 可能会被分割成多分并行计算,所以这里处理当 value2 传入的是某个rdd某个部分计算的值
            value = {k: v + value2[k] for k, v in value1.items()}
            return value
        else:
            if value1.get(value2) is not None:
                value1[value2] += 1
        return value1


sc = SparkContext("local")
accum = sc.accumulator("", accum_param=MyAccum())

rdd = sc.parallelize(["a", "b", "a", "c", "e", "d", "c"])
rdd = rdd.map(lambda x: accum.add(x))
rdd.count()
print(accum.value)
