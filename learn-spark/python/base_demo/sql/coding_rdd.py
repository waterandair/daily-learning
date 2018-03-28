from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType
spark = SparkSession\
    .builder\
    .appName("coding_rdd")\
    .getOrCreate()

sc = spark.sparkContext

lines = sc.textFile("file:///usr/local/spark-2.2.1/examples/src/main/resources/people.txt")
parts = lines.map(lambda l: l.split(","))
people = parts.map(lambda p: (p[0], p[1].strip()))

# 定义 schema
schemaString = "name age"

fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)

schemaPeople = spark.createDataFrame(people, schema)
# 必须注册为临时表才能供下面查询使用
schemaPeople.createOrReplaceTempView("people")
results = spark.sql("SELECT name FROM people")
results.show()