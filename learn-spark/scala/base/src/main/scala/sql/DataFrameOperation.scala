package sql

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.Row

object DataFrameOperation {
  case class Person(name: String, age: Long)
  case class Person2(id:Long, name: String, age: Long)

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("DataFrameCreate")
    val sc = new SparkContext(conf)

    val spark = SparkSession
      .builder()
      .getOrCreate()

    /**
      * 用于一些隐式转换, 比如把 RDDS 转换为 DataFrames
      */
    import spark.implicits._

    val df = spark.read.json("hdfs://localhost:9000/user/zj/spark/students.json")

    /**
      * 结构化的显示内容
      */
    df.show()

    // print the schema in a thee format
    df.printSchema()

    // select only the "name" column
    df.select("name").show()

    // select everybody, but increment the age by 1
    df.select($"name", $"age" + 1).show()

    // select people older than 18
    df.filter($"age" > 18).show()

    // count people by age
    df.groupBy("age").count().show()

    // Register the DataFrame as a SQL temporary view
    df.createOrReplaceTempView("people")

    val sqlDF = spark.sql("SELECT * FROM people")
    sqlDF.show()

    /**
      * register the DataFrame as a global temporary view
      * Global temporary view is tied(约束) to a system preserved database global_temp, and we must use the
      * qualified name of refer it
      * 使用全局视图,必须加上 global_temp
      */
    df.createGlobalTempView("people")
    spark.sql("SELECT * FROM global_temp.people").show()
    // Global temporary view is cross-session
    spark.newSession().sql("SELECT * FROM global_temp.people").show()

    /**
      * creating Datasets
      * Datasets are similar to RDDs
      * use a specialized Encoder to serialized Encoder to serialize the objects for processing or
      * transmitting over the network
      * Encoders are code generated dynamically and use a format that allows Spark to perform many operations
      * like filtering, sorting, and hashing without deserializing the bytes back into an object
      */
    // case class Person(name: String, age: Long)
    // Move case class outside of the method: case class, by use of which you define the schema of the DataFrame,
    // should be defined outside of the method needing it.
    // You can read more about it here: https://issues.scala-lang.org/browse/SI-6649
    val caseClassDS = Seq(Person("zj", 24)).toDS()
    caseClassDS.show()

    // Encoders for most common types are automatically provided by importing spark.implicits._
    val primitiveDS = Seq(1, 2, 3).toDS()
    primitiveDS.map(_ + 1).collect()

    // DataFrames can be converted to a DataSet by providing a class. Mapping will we be done by name
    val path = "hdfs://localhost:9000/user/zj/spark/students.json"
    val peopleDS = spark.read.json(path).as[Person2]
    peopleDS.show()

    /**
      * Inter operating with RDDs
      *
      */
    // 1. 反射方式
    val peopleRDD = sc.textFile("hdfs://localhost:9000/user/zj/spark/students.txt")
    val peopleDF = peopleRDD
      .map(_.split(","))
      .map(row => Person2(row(0).toInt, row(1), row(2).toInt))
      .toDF()
      .createOrReplaceTempView("people")

    val teenagersDF = spark.sql("SELECT name, age FROM people WHERE age BETWEEN 0 AND 18")
    teenagersDF.show()

    // The columns of a row in the result can be accessed by field index
    teenagersDF.map(teenager => "Name " + teenager(1)).show()
    // or by field name
    teenagersDF.map(teenager => "Name:" + teenager.getAs[String]("name")).show()

    // 2. 编程方式
    // (1) 构造出元素为 Row 的普通RDD
    val rowRDD = peopleRDD
      .map(_.split(","))
      .map(attr => Row(attr(0).toInt, attr(1), attr(2).toInt))
    // (2)编程方式动态构造元数据
    val structType = StructType(Array(
      StructField("id", IntegerType, nullable = true),
      StructField("name", StringType, nullable = true),
      StructField("age", IntegerType, nullable = true)
    ))
    // (3) 进行RDD到DataFrame的转换
    spark.createDataFrame(rowRDD, structType).createOrReplaceTempView("people")

    spark.sql("SELECT name FROM people").show()


    /**
      * Aggregations
      * The built-in DataFrames functions provide common aggregations such as count(), countDistinct(), avg(), max(), min(),
      */
    // Untyped User-Defined Aggregate Functions 见 sql/udf






  }
}
