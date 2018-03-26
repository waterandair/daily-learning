#!/usr/bin/python3
# -*- coding utf-8 -*-
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

sc = SparkContext("local[4]", "streaming-kafka")
ssc = StreamingContext(sc, batchDuration=3)

zkQuorum = "172.17.0.2:2181"
group_id = "group-5"
topics = {
    "test": 1
}

kafkaStream = KafkaUtils.createStream(ssc, zkQuorum, group_id, topics)

word_counts = kafkaStream\
    .map(lambda x: x[1])\
    .flatMap(lambda line: line.split(" "))\
    .map(lambda word: (word, 1))\
    .reduceByKey(lambda a, b: a + b)

word_counts.pprint()

ssc.start()
ssc.awaitTermination()


