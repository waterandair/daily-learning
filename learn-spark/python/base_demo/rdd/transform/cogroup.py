from pyspark import SparkContext
import pyspark.resultiterable
if __name__ == '__main__':
    sc = SparkContext()
    rdd_1 = sc.parallelize([
        (1, 1),
        (1, True),
    ])
    rdd_2 = sc.parallelize([
        (1, "1"),

    ])
    rdd_3 = sc.parallelize([

    ])
    # 在一个 (K, V) 和的 dataset 上调用时，返回一个 (K, (Iterable<V>, Iterable<W>)) tuples 的 dataset. 这个操作也调用了 groupWith.

    rdd_cogroup = rdd_1.cogroup(rdd_2)

    res = [(x, tuple(map(list, y))) for x, y in sorted(list(rdd_cogroup.collect()))]
    print(res)  # [(1, ([1, True], ['1']))]


