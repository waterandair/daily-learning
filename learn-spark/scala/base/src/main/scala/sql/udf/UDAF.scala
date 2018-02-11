package sql.udf

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.sql.types.StructType
import org.apache.spark.sql.types.StructField
import org.apache.spark.sql.types.StringType

case class Employee(name: String, salary: Long)
case class Average(var sum: Long, var count: Long)

object UDAF {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("UDAF")
    val sc = new SparkContext(conf)
    val spark = SparkSession
      .builder()
      .getOrCreate()

    //strCount(sc, spark)
    //myAverage(sc, spark)
    myAverage2(sc, spark)




  }

  def strCount(sc: SparkContext, spark: SparkSession): Unit ={
    // 构造模拟数据
    val names = Array("Leo", "Marry", "Jack", "Tom", "Tom", "Tom", "Leo")
    val namesRDD = sc.parallelize(names)
    val namesRowRDD = namesRDD.map(name => Row(name))
    val structType = StructType(Array(
      StructField("name", StringType, nullable = true)
    ))
    val namesDF = spark.createDataFrame(namesRowRDD, structType)

    // 注册一张 names 表
    namesDF.createOrReplaceTempView("names")

    // 定义和注册自定义函数
    spark.udf.register("strCount", new StringCount)

    // 使用自定义函数
    spark.sql("SELECT name, strCount(name) from names group by name")
      .collect()
      .foreach(println)
  }

  def myAverage(sc: SparkContext, spark: SparkSession): Unit ={
    val df = spark.read.json("hdfs://localhost:9000/user/zj/spark/employees.json")
    df.createOrReplaceTempView("employees")

    spark.udf.register("myAverage", new MyAverage)

    val res = spark.sql("SELECT myaverage(salary) as average_salary FROM employees ")
    res.show()
  }

  def myAverage2(sc: SparkContext, spark: SparkSession): Unit = {
    import spark.implicits._
    val ds = spark.read.json("hdfs://localhost:9000/user/zj/spark/employees.json").as[Employee]
    val averageSalary = new MyAverage2().toColumn.name("average_salary")
    val result = ds.select(averageSalary)
    result.show()
  }

}
