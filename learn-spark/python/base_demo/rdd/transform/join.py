from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()
    x = sc.parallelize([("a", 1), ("b", 4)])
    y = sc.parallelize([("a", 2), ("a", 3), ("c", 5)])

    print("join:", sorted(x.join(y).collect()))  # [('a', (1, 2)), ('a', (1, 3))]
    print("leftOuterJoin:", sorted(x.leftOuterJoin(y).collect()))  # [('a', (1, 2)), ('a', (1, 3)), ('b', (4, None))]
    print("rightOuterJoin:", sorted(x.rightOuterJoin(y).collect()))  # [('a', (1, 2)), ('a', (1, 3)), ('c', (None, 5))]
    print("fullOuterJoin:", sorted(x.fullOuterJoin(y).collect()))  # [('a', (1, 2)), ('a', (1, 3)), ('b', (4, None)), ('c', (None, 5))]
