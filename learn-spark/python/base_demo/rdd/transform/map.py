from pyspark import SparkContext
from pyspark import SparkConf

if __name__ == '__main__':
    conf = SparkConf()
    conf.set("spark.default.parallelism", "500")
    sc = SparkContext("local[2]", conf=conf)
    sc.setLogLevel("OFF")
    rdd = sc.parallelize(["a", "b", "c"])
    # 将原来RDD的每个数据项通过map中的用户自定义函数f映射转变为一个新的元素
    rdd_upper = rdd.map(lambda x: str(x).upper())

    rdd_upper.foreach(lambda x: print(x))  # A, B, C