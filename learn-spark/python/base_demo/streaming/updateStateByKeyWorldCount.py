#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from pyspark.streaming import StreamingContext
from pyspark import SparkContext

sc = SparkContext("local[2]", "streaming_socket")
ssc = StreamingContext(sc, 10)
ssc.checkpoint("hdfs://127.0.0.1:9000/wordcount_checkpoint")

lines = ssc.socketTextStream("localhost", 9999)
words = lines\
    .flatMap(lambda l: l.split())\
    .map(lambda w: (w, 1))


def word_count(values, state):
    if not state:
        state = 0
    for value in values:
        state += value
    return state


wordcount = words.updateStateByKey(word_count)
wordcount.pprint()

ssc.start()
ssc.awaitTermination()
