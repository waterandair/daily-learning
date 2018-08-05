from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()
    rdd = sc.parallelize([(1, "a"), (1, "a"), (1, "a"), (2, "b"), (2, "b"), (3, "c")])
    rdd_groupbykey = rdd.groupByKey()

    # 在一个 (K, V) pair 的 dataset 上调用时，返回一个 (K, Iterable<V>)
    # 如果分组是为了在每一个 key 上执行聚合操作（例如，sum 或 average)，此时使用 reduceByKey 或 aggregateByKey 来计算性能会更好.
    # 默认情况下，并行度取决于父 RDD 的分区数。可以传递一个可选的 numTasks 参数来设置不同的任务数
    rdd_groupbykey.foreach(lambda x: print(x[0], x[1]))
    # 1 ['a', 'a', 'a']
    # 2 ['b', 'b']
    # 3 ['c']
