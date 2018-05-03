#!/usr/bin/python3
# -*- coding utf-8 -*-
from pyspark import SparkContext
sc = SparkContext('local', 'test')
logFile = "file:///usr/local/spark-2.2.1/README.md"
logData = sc.textFile(logFile, 2).cache()
numAs = logData.filter(lambda line: 'a' in line).count()
numBs = logData.filter(lambda line: 'b' in line).count()
print('Lines with a: %s, Lines with b: %s' % (numAs, numBs))