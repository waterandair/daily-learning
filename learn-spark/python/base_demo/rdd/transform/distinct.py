from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()
    rdd = sc.parallelize(["1", "1", "2", "3", 1, 1, 2])
    # 对数据源中的元素进行去重, 数字字符串不会隐式转换
    rdd_distinct = rdd.distinct()
    print(rdd_distinct.collect())  # ['3', 1, '1', 2, '2']
