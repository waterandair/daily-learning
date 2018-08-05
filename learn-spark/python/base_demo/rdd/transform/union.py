from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()
    rdd_a = sc.parallelize(["1", "2", "3"])
    rdd_b = sc.parallelize(["a", "b", "c", "1"])
    # 合并两个RDD，不去重,返回两个数据源的并集
    rdd_union = rdd_a.union(rdd_b)  # ['1', '2', '3', 'a', 'b', 'c', '1']
    print(rdd_union.collect())