from pyspark import SparkContext
from pyspark.streaming import StreamingContext

#local[*] 中必须设置大于1的并行数量
sc = SparkContext("local[2]", "streaming")
# 设置每次计算的时间间隔
ssc = StreamingContext(sc, 5)
lines = ssc.textFileStream('file:///home/zj/logs')
words = lines.flatMap(lambda l: l.split())
wordsPair = words.map(lambda x: (x, 1))
wordscount = wordsPair.reduceByKey(lambda a, b: a + b)
wordscount.pprint()

ssc.start()
ssc.awaitTermination()

