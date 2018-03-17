#!/usr/bin/python3
# -*- coding utf-8 -*-
from pyspark import SparkContext
sc = SparkContext('local[4]', 'rdd_demo')
# RDD可以通过两种方式创建：
# * 第一种：读取一个外部数据集。比如，从本地文件加载数据集，或者从HDFS文件系统、HBase、Cassandra、Amazon S3等外部数据源中加载数据集。
#          Spark可以支持文本文件、SequenceFile文件（Hadoop提供的 SequenceFile是一个由二进制序列化过的key/value的字节流组成的文本存
#          储文件）和其他符合Hadoop InputFormat格式的文件。
# * 第二种：调用SparkContext的parallelize方法，在Driver中一个已经存在的集合（数组）上创建。

# 从文件中读取
file = sc.textFile('file:///home/zj/...')
# 从hdfs中读取
file = sc.textFile('/user/zj/***.txt')
# 从 json 文件中解析 json
# {"name":"Michael"}
# {"name":"Andy", "age":30}
# {"name":"Justin", "age":19}
import json
sc = SparkContext('local','JSONAPP')
inputFile =  "file:///home/dblab/people.json"
jsonStrs = sc.textFile(inputFile)
result = jsonStrs.map(lambda s: json.loads(s))
# 直接创建(测试时用)
nums = [1, 2, 3, 4, 5]
rdd = sc.parallelize(nums)

# 持久化
jsonStrs.persist('MEMORY_ONLY')  # 相当于 rdd.cache()

# 打印元素
# 可以使用collect()方法，比如，rdd.collect().foreach(print)，但是，由于collect()方法会把各个worker节点上的所有RDD元素都抓取
# 到Driver Program中，因此，这可能会导致内存溢出。因此，当你只需要打印RDD的部分元素时，可以采用语句rdd.take(100).foreach(print)。

# 共享变量
#   广播变量
broadcastVar = sc.broadcast([1, 2, 3])
broadcastVar.value  # [1,2,3]

# 累加器
accum = sc.accumulator(0)
sc.parallelize([1, 2, 3, 4]).foreach(lambda x : accum.add(x))
accum.value  # 10
