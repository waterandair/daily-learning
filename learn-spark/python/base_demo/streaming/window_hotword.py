#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext("local[2]", "window_hotword")
ssc = StreamingContext(sc, 5)
ssc.checkpoint("hdfs://127.0.0.1:9000/window_checkpoint")

# 接收实时的搜索词数据, 格式 "name word"
search_logs_dstream = ssc.socketTextStream("127.0.0.1", 9999)
# 将日志转换为只有一个搜索词
search_words_dstream = search_logs_dstream.map(lambda line: line.split(" ")[1])
# 将搜索词映射为 (word, 1) 的格式
search_word_pairs_dstream = search_words_dstream.map(lambda word: (word, 1))

# 对 search_word_pairs_dstream 进行窗口操作
"""
python 的 reduceByKeyAndWindow 和 scala/java 的略有不同,
    scala/java 只传一个进行reduce的函数
    python 需要传两个, 第一个表示对新进入 window 的 batch 进行的reduce 操作, 第二个表示对离开 window 的 batch 进行的 reduce 操作
    第二个参数可以为None, 这样就表示要对window中所有的 batch 执行 reduce 操作,这样相对来说会降低性能,特别是在滑动间隔比较长的时候
    
"""
search_word_count_dstream = search_word_pairs_dstream.reduceByKeyAndWindow(lambda a, b: a+b, lambda a, b: a-b, 30, 10)


def transform(rdd):
    # 将 rdd 转换为 (count, word) 格式
    count_word_rdd = rdd.map(lambda row: (row[1], row[0]))
    # 对 key 进行倒序排序
    sorted_rdd = count_word_rdd.sortByKey(False)
    # 将 rdd 转换为 (word, count) 格式
    word_count_rdd = sorted_rdd.map(lambda row: (row[1], row[0]))
    # 取前三
    top3_word_count = word_count_rdd.take(3)
    rdd = word_count_rdd.filter(lambda row: row in top3_word_count)
    # for word_count in top3_word_count:
    #     print("***********" + str(word_count) + "*************")
    return rdd


# 对 window 中的词频进行排序
final_dstream = search_word_count_dstream.transform(lambda rdd: transform(rdd))

final_dstream.pprint()

ssc.start()
ssc.awaitTermination()

