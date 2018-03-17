from pyspark.streaming import StreamingContext
from pyspark import SparkContext

sc = SparkContext("local[2]", "streaming_socket")
ssc = StreamingContext(sc, 10)

lines = ssc.socketTextStream("localhost", 9999)
wordcount = lines\
    .flatMap(lambda l: l.split())\
    .map(lambda w: (w, 1))\
    .reduceByKey(lambda a, b: a + b)

wordcount.pprint()

ssc.start()
ssc.awaitTermination()