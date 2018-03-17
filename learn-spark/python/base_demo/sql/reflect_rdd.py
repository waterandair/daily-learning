from pyspark.sql import SparkSession
from pyspark.sql.types import Row

spark = SparkSession\
    .builder \
    .appName("reflect rdd to dataFrame") \
    .getOrCreate()
sc = spark.sparkContext
# Michael, 29
# Andy, 30
# Justin, 19
lines = sc.textFile("file:///usr/local/spark-2.2.1/examples/src/main/resources/people.txt")
parts = lines.map(lambda l: l.split(","))
people = parts.map(lambda p: Row(name=p[0], age=int(p[1].strip())))

schemaPeople = spark.createDataFrame(people)
# 必须注册为临时表才能供下面的查询使用
schemaPeople.createOrReplaceTempView("people")

teenagers = spark.sql("SELECT name FROM people WHERE age >= 13 AND age <=19")

teenNames = teenagers.rdd.map(lambda p: "Name: " + p.name).collect()
for name in teenNames:
    print(name)