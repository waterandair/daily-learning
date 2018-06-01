#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql.types import Row
from pyspark.sql import SparkSession

"""
案例: top3 热门商品实时统计
"""
sc = SparkContext("local[2]", "steaming_sql_top3")
ssc = StreamingContext(sc, 5)
ssc.checkpoint("hdfs://127.0.0.1:9000/checkpoint/steaming_sql_top3/")


# 接收点击数据 "username product category"
product_click_logs_dstream = ssc.socketTextStream("127.0.0.1", 9999)

# 映射为 (category_product, 1), 方便进行window操作统计每种类别的每个商品的点击次数
category_pro_dstream = product_click_logs_dstream.map(lambda row: (row.split(" ")[2] + "_" + row.split(" ")[1], 1))

# 执行 window 操作, 每隔 60 秒统计每个种类每个商品的点击次数
category_pro_counts_dstream = category_pro_dstream.reduceByKeyAndWindow(lambda a, b: a+b, lambda a, b: a-b, 60, 10)


def top3(rdd):
    # 使用反射推断Schema
    rdd = rdd.map(lambda row: Row(category=row[0].split("_")[0], product=row[0].split("_")[1], click_count=row[1]))
    spark = SparkSession \
        .builder \
        .appName("steaming_sql_top3") \
        .getOrCreate()
    # rdd 转换为 dataFrame
    category_pro_counts_schema = spark.createDataFrame(rdd)
    # 注册为临时表
    category_pro_counts_schema.createOrReplaceTempView("product_click_log")
    # top3
    top3_product_df = spark.sql(
        "SELECT * FROM ("
            "SELECT *, row_number() OVER (PARTITION BY category ORDER BY click_count DESC) rank "
                "FROM product_click_log ) tmp "
        "WHERE rank <= 3")
    top3_product_df.show()


category_pro_counts_dstream.foreachRDD(lambda rdd: top3(rdd))

ssc.start()
ssc.awaitTermination()
# ssc.stop(True, True)

"""
测试数据:  nc -lk 9999
zj iphone1 phone 
zj iphone2 phone 
zj iphone2 phone
zj iphone3 phone
zj iphone3 phone
zj iphone3 phone
zj iphone4 phone
zj iphone4 phone
zj iphone4 phone
zj iphone4 phone
zj car1 car
zj car2 car
zj car2 car
zj car3 car
zj car3 car
zj car3 car
zj car4 car
zj car4 car
zj car4 car
zj car4 car
zj shoes1 shoes
zj shoes2 shoes
zj shoes2 shoes
zj shoes3 shoes
zj shoes3 shoes
zj shoes3 shoes
zj shoes4 shoes
zj shoes4 shoes
zj shoes4 shoes
zj shoes4 shoes
"""

"""
返回结果:
+--------+-----------+-------+----+                                             
|category|click_count|product|rank|
+--------+-----------+-------+----+
|   shoes|          4| shoes4|   1|
|   shoes|          3| shoes3|   2|
|   shoes|          2| shoes2|   3|
|   phone|          4|iphone4|   1|
|   phone|          3|iphone3|   2|
|   phone|          2|iphone2|   3|
|     car|          4|   car4|   1|
|     car|          3|   car3|   2|
|     car|          2|   car2|   3|
+--------+-----------+-------+----+
"""
