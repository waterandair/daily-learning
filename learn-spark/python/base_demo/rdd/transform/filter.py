from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext()

    rdd = sc.parallelize(["a", "b", "c"])
