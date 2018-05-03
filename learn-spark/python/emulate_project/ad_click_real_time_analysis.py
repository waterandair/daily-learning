#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

sc = SparkContext(master='local[2]', appName='ad_click_real_time_analysis')
ssc = StreamingContext(sc, 5)  # 每 5 秒一个batch

# 从 kafka 中读取数据
group_id = "group-1"
topics = {
    "ad_click": 1
}
zkQuorum = "127.0.0.1:2181"
ad_real_time_log_DStream = KafkaUtils.createStream(ssc, zkQuorum, group_id, topics)

# 原始数据为 <timestamp, province, city, userid, adid> , 转换为 <yyyyMMdd_userid_adid> 的形式


