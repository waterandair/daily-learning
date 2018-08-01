from pyspark import SparkContext
import datetime
if __name__ == '__main__':
    sc = SparkContext()
    rdd = sc.parallelize(range(20))

    # 样本数据，设置是否放回（withReplacement）,
    # 采样的百分比（fraction）、
    # 使用指定的随机数生成器的种子（seed）,比如当前时间戳.
    sample_rdd = rdd.sample(False, 0.5, int(datetime.datetime.now().timestamp()))
    print(sample_rdd.collect())  # [0, 4, 5, 8, 9, 12, 13, 16, 17] 不一定是严格按照采样比例的