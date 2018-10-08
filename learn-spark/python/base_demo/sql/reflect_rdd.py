from pyspark.sql import SparkSession
from pyspark.sql.types import Row

spark = SparkSession\
    .builder \
    .appName("reflect rdd to dataFrame") \
    .getOrCreate()
sc = spark.sparkContext

lines = sc.parallelize([
    "Michael, 29",
    "Andy, 30",
    "Justin, 19",
])

parts = lines.map(lambda l: l.split(","))
people = parts.map(lambda p: Row(name=p[0], age=int(p[1].strip())))

schemaPeople = spark.createDataFrame(people)

# 必须注册为临时表才能供下面的查询使用
schemaPeople.createOrReplaceTempView("people")

# 返回 dataframe
teenagers = spark.sql("SELECT name FROM people WHERE age >= 13 AND age <=19")

teenagers.show()
# +------+
# |  name|
# +------+
# |Justin|
# +------+

# 将 dataframe 再转为 rdd
teenNames = teenagers.rdd.map(lambda p: "Name: " + p.name).collect()
for name in teenNames:
    print(name)
# Name: Justin