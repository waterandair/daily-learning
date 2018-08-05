from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()

    rdd = sc.parallelize([
        "a b c d e f g",
        "h i g k l m n",
    ])

    # 与map类似，但每个输入的RDD成员可以产生0或多个输出成员, lambda 函数中返回的应该是一个序列而不是一个单独的元素
    flatMap_rdd = rdd.flatMap(lambda x: str(x).split())

    print(flatMap_rdd.count())  # 14
