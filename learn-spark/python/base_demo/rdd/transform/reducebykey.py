from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()
    rdd = sc.parallelize([
        ("a", 1),
        ("b", 1),
        ("c", 1),
        ("a", 1),
        ("a", 1),
        ("b", 1),
        ("c", 1),
        ("a", 1),
        ("a", 1),
        ("a", 1),
    ])
    # 在 (K, V) pairs 的 dataset 上调用时, 返回 dataset of (K, V) pairs 的 dataset,
    # 其中的 values 是针对每个 key 使用给定的函数 func 来进行聚合的, 它必须是 type (V,V) => V 的类型.
    # 像 groupByKey 一样, reduce tasks 的数量是可以通过第二个可选的参数来配置的.

    rdd_reducebykey = rdd.reduceByKey(lambda a, b: a + b)
    print(rdd_reducebykey.collect())  # [('b', 2), ('c', 2), ('a', 6)]
