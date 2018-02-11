package sql

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession

object DataFrameCreate {
  def main(args: Array[String]): Unit = {
    var conf = new SparkConf()
      .setMaster("local")
      .setAppName("DataFrameCreate")
    var sc = new SparkContext(conf)

    val spark = SparkSession
      .builder()
      .appName("Spark SQL basic example")
      .config("spark.some.config.option", "some-value")
      .getOrCreate()

    import spark.implicits._

    val df = spark.read.json("hdfs://localhost:9000/user/zj/spark/students.json")

    df.show()
  }
}
