import os
import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# 在Spark Streaming中, 无法从 checkpoint 恢复 Accumulators 和 Broadcast 变量 . 如果启用 checkpoint 并使用 Accumulators 或
# Broadcast 变量 , 则必须为 Accumulators 和 Broadcast 变量创建延迟实例化的单例实例, 以便在 driver 重新启动失败后重新实例化.
# Get or register a Broadcast variable
def getWordBlacklist(sparkContext):
    if ('wordBlacklist' not in globals()):
        globals()['wordBlacklist'] = sparkContext.broadcast(["a", "b", "c"])
    return globals()['wordBlacklist']


# Get or register an Accumulator
def getDroppedWordsCounter(sparkContext):
    if ('droppedWordsCounter' not in globals()):
        globals()['droppedWordsCounter'] = sparkContext.accumulator(0)
    return globals()['droppedWordsCounter']


def createContext(host, port, outputPath):
    # If you do not see this printed, that means the StreamingContext has been loaded from the new checkpoint
    print("Creating new context")
    if os.path.exists(outputPath):
        os.remove(outputPath)
    sc = SparkContext(appName="PythonStreamingRecoverableNetworkWordCount")
    ssc = StreamingContext(sc, 10)

    lines = ssc.socketTextStream(host, port)
    words = lines.flatMap(lambda line: line.split(" "))
    wordCounts = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)

    def echo(time, rdd):
        # Get or register the blacklist Broadcast
        blacklist = getWordBlacklist(rdd.context)
        # Get or register the droppedWordsCounter Accumulator
        droppedWordsCounter = getDroppedWordsCounter(rdd.context)

        # Use blacklist to drop words and use droppedWordsCounter to count them
        def filterFunc(wordCount):
            if wordCount[0] in blacklist.value:
                droppedWordsCounter.add(wordCount[1])
                return False
            else:
                return True

        counts = "Counts at time %s %s" % (time, rdd.filter(filterFunc).collect())
        print(counts)
        print("Dropped %d word(s) totally" % droppedWordsCounter.value)
        print("Appending to " + os.path.abspath(outputPath))
        with open(outputPath, 'a') as f:
            f.write(counts + "\n")

    wordCounts.foreachRDD(echo)
    return ssc


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: recoverable_network_wordcount.py <hostname> <port> "
              "<checkpoint-directory> <output-file>", file=sys.stderr)
        sys.exit(-1)
    host, port, checkpoint, output = sys.argv[1:]
    ssc = StreamingContext.getOrCreate(checkpoint, lambda: createContext(host, int(port), output))
    ssc.sparkContext.setLogLevel("ERROR")
    ssc.start()
    ssc.awaitTermination()