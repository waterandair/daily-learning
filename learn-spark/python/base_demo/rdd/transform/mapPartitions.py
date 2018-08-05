from pyspark import SparkContext
from pyspark import TaskContext

if __name__ == '__main__':
    sc = SparkContext()
    tc = TaskContext()

    rdd = sc.parallelize(["这", "是", "一", "首", "简", "单", "的", "小", "情", "歌"], 3)

    # 与map类似，map是作用于每个元素，而 mapPartitions 是作用于每个分区
    # mapPatririons 的函数参数和返回值的类型都应该是 iterator
    def f(iter):
        yield "".join(iter) + str(tc.partitionId())
    mapPartitions_rdd = rdd.mapPartitions(f)

    print(mapPartitions_rdd.collect())  # ['这是一0', '首简单1', '的小情歌2']
