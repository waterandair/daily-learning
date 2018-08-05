from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()
    rdd_1 = sc.parallelize([(1, "a"), (2, "b")])
    rdd_2 = sc.parallelize([(1, "A"), (2, "B")])

    # 笛卡尔积
    rdd_cartesian = rdd_1.cartesian(rdd_2)
    print(rdd_cartesian.collect())
    # [((1, 'a'), (1, 'A')), ((1, 'a'), (2, 'B')), ((2, 'b'), (1, 'A')), ((2, 'b'), (2, 'B'))]