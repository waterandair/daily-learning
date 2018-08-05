from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()
    rdd = sc.parallelize([
        (6, "a"),
        (1, "a"),
        (6, "b"),
        (4, "c"),
        (4, "a"),
        (2, "a"),
    ])

    rdd_sortByKey = rdd.sortByKey(True)
    print(rdd_sortByKey.collect())  # [(1, 'a'), (2, 'a'), (4, 'c'), (4, 'a'), (6, 'a'), (6, 'b')]