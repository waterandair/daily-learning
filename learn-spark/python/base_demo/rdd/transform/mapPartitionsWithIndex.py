from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()

    rdd = sc.parallelize(["这", "是", "一", "首", "简", "单", "的", "小", "情", "歌"], 3)

    def f(i, iter):
        yield str(i) + "".join(iter)

    def f2(i, itera):
        for x in itera:
            yield i, x

    # 与 mapPartitions 类似, 这是多传入一个代表分区索引的参数
    mapPartitionsWithIndex_rdd = rdd.mapPartitionsWithIndex(f)
    mapPartitionsWithIndex_rdd2 = rdd.mapPartitionsWithIndex(f2)

    print(mapPartitionsWithIndex_rdd.collect())  # ['0这是一', '1首简单', '2的小情歌']

    mapPartitionsWithIndex_rdd2.foreach(lambda x: print(x))
    # (0, '这')
    # (1, '首')
    # (1, '简')
    # (0, '是')
    # (1, '单')
    # (0, '一')
    # (2, '的')
    # (2, '小')
    # (2, '情')
    # (2, '歌')

