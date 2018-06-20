#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def daily_user_ad_click_dstream(row):
    log = row[1]
    log_list = log.split(" ")

    timestamp = log_list[0]


if __name__ == '__main__':

    sc = SparkContext(master='local[2]', appName='ad_click_real_time_analysis')
    ssc = StreamingContext(sc, 5)  # 每 5 秒一个batch

    # 从 kafka 中读取数据
    group_id = "group-1"
    topics = ['ad_real_time_log']
    kafkaParams = {
        "metadata.broker.list": "127.0.0.1:9092",
    }
    ad_real_time_log_DStream = KafkaUtils.createDirectStream(ssc, topics, kafkaParams)
    daily_user_ad_click_DStream = ad_real_time_log_DStream.map(lambda row: daily_user_ad_click_dstream(row))

    ad_real_time_log_DStream.pprint()

    # 原始数据为 <timestamp, province, city, userid, adid> , 转换为 <yyyyMMdd_userid_adid, 1> 的形式


    ssc.start()
    ssc.awaitTermination()

