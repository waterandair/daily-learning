#!/usr/bin/python3
# -*- coding utf-8 -*-
from pyspark import SparkContext
sc = SparkContext('local', 'wordcount')
# hdfs dfs -put ./word.txt .
textFile = sc.textFile("word.txt")
wordcount = textFile.flatMap(lambda line: line.split(" "))\
    .map(lambda word: (word, 1))\
    .reduceByKey(lambda a, b: a + b)

wordcount.foreach(print)