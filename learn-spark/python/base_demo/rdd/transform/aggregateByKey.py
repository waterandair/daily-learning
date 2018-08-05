from pyspark import SparkContext


if __name__ == '__main__':
    sc = SparkContext()
    rdd = sc.parallelize([
        (1, 3),
        (1, 2),
        (1, 4),
        (2, 3)
    ], 2)

    # reduceByKey 可以认为是 aggregateByKey 的简化版
    # aggregateByKey 多提供一个 Seq Function,可以由用户自己控制如何对每个 partition 中的数据进行先聚合，
    #                然后再对所有partition中的数据进行全局聚合
    #   参数：
    #       zeroValue： Key 的初始值
    #       seqOp：进行 shuffle map-side 的本地聚合函数
    #       combOp：进行 shuffle reduce-side 的全局聚合

    # 这个例子中，将[(1, 3), (1, 2), (1, 4), (2, 3)] 分为了 2 个 partition
    #               partition1: [(1, 3), (1, 2)]
    #               partition2: [(1, 4), (2, 3)]
    # 执行过程：
    #         1. 在各自partition中先执行 lambda a, b: max(a, b) , 进行本地聚合, 各自执行的结果为：
    #               partition1: [(1, 3)]
    #               partition2: [(1, 4), (2, 3)]
    #         2. partitions 执行 lambda a, b: a + b 全局聚合， 执行结果为： [(2, 3), (1, 7)]
    #
    rdd_aggregateByKey = rdd.aggregateByKey(0, lambda a, b: max(a, b), lambda a, b: a + b)
    print(rdd_aggregateByKey.collect())  # [(2, 3), (1, 7)]
