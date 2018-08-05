from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()

    rdd = sc.parallelize(["a", "B", "c"])
    # 对元素进行过滤，对每个元素应用f函数，返回值为true的元素在RDD中保留，返回为false的将过滤掉
    filter_rdd = rdd.filter(lambda x: str(x).islower())
    print(filter_rdd.collect())  # ['a', 'c']