from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext("local[2]")
    sc.setLogLevel("OFF")
    rdd = sc.parallelize(["a", "b", "c"])
    # 将原来RDD的每个数据项通过map中的用户自定义函数f映射转变为一个新的元素
    rdd_upper = rdd.map(lambda x: str(x).upper())

    rdd_upper.foreach(lambda x: print(x))