import time
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext("local[4]", "streaming_rdds")
ssc = StreamingContext(sc, 1)

queue = []

for i in range(10):
    queue += [ssc.sparkContext.parallelize([j for j in range(1, 1001)], 10)]

wordcount = ssc.queueStream(queue).map(lambda x: (x % 10, 1)).reduceByKey(lambda a, b: a + b)
wordcount.pprint()

ssc.start()
time.sleep(10)

# stopGracefully, 等待所有任务完成
ssc.stop(stopSparkContext=True, stopGraceFully=True)
