from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()
    rdd_a = sc.parallelize([1, 2, 3, 8, 9])
    rdd_b = sc.parallelize(["1", "2", "3", 4, 8])

    # 返回两个 rdd 的交集, 数字字符串会隐式转换
    rdd_intersection = rdd_a.intersection(rdd_b)
    print(rdd_intersection.collect())  # [8]
