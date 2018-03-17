from pyspark.sql import SparkSession
from pyspark.sql.types import Row

spark = SparkSession\
    .builder\
    .appName("write_DF_to_mysql")\
    .getOrCreate()
sc = spark.sparkContext

peoplelist = [
    "zj 25",
    "kobe 41"
]
peopleRDD = sc.parallelize(peoplelist)
people = peopleRDD\
    .map(lambda l: l.split())\
    .map(lambda p: Row(name=p[0], age=p[1]))

peopleDF = spark.createDataFrame(people)

peopleDF.write\
    .format("jdbc")\
    .option("url", "jdbc:mysql://localhost:3306/spark")\
    .option("dbtable", "people") \
    .option("user", "root") \
    .option("password", "000000") \
    .option("driver", "com.mysql.jdbc.Driver") \
    .mode("append")\
    .save()


# prop = {
#     'user': 'root',
#     'password': '000000',
#     'driver': 'com.mysql.jdbc.Driver'
# }
# peopleDF.write\
#     .jdbc("jdbc:mysql://localhost:3306/spark",'people','append', prop)



