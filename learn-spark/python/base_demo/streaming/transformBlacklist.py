#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from pyspark.streaming import StreamingContext
from pyspark import SparkContext

sc = SparkContext("local[2]", "transformBlacklist")
ssc = StreamingContext(sc, 5)

blacklist = [
    ("tom", True),
    ("jerry", True)
]
# 模拟一个黑名单 (姓名, 是否启用)
blacklistRdd = sc.parallelize(blacklist)
# 接收实时访问日志, 这里简化为格式为 "date username
logDStream = ssc.socketTextStream("127.0.0.1", 9999)

# 把 "data username" 转为 (username, "date username)
userLogDStream = logDStream.map(lambda row: (row.split(" ")[1], row))


def transform(rdd):
    joinedRdd = rdd.leftOuterJoin(blacklistRdd)
    filteredRdd = joinedRdd.filter(lambda row: row[1][1] is not True)
    validLogRdd = filteredRdd.map(lambda row: row[1])
    return validLogRdd


validLogDStream = userLogDStream.transform(lambda rdd: transform(rdd))

validLogDStream.pprint()

ssc.start()
ssc.awaitTermination()
