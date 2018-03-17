from pyspark.sql import SparkSession

spark = SparkSession\
    .builder\
    .appName("coding_rdd")\
    .getOrCreate()

jdbcDF = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark") \
    .option("dbtable", "people") \
    .option("user", "root") \
    .option("password", "000000") \
    .option("driver", "com.mysql.jdbc.Driver") \
    .load()

jdbcDF.show()