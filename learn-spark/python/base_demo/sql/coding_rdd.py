from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType
spark = SparkSession\
    .builder\
    .appName("coding_rdd")\
    .getOrCreate()

sc = spark.sparkContext

lines = sc.parallelize([
    "Michael, 29",
    "Andy, 30",
    "Justin, 19",
])

people = lines.map(lambda l: tuple(l.split(",")))

# 定义 schema
schemaString = "name age"

fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)
schemaPeople = spark.createDataFrame(people, schema)

# 必须注册为临时表才能供下面查询使用
schemaPeople.createOrReplaceTempView("people")
results = spark.sql("SELECT * FROM people")
results.show()
# +-------+---+
# |   name|age|
# +-------+---+
# |Michael| 29|
# |   Andy| 30|
# | Justin| 19|
# +-------+---+
