package test
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.sql.{Row, SparkSession}

import scala.collection.mutable.ArrayBuffer


object App {
  case class Data(id:Int, grp1:String, grp2:String, idvar:Int)
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName("derive")
      .setMaster("local")
    val sc = new SparkContext(conf)
    val spark = SparkSession
      .builder()
      .getOrCreate()

    import spark.implicits._

    val arr = Array(
      "0 a e 1",
      "1 b f 1",
      "2 c e 1",
      "3 d f 1",
      "4 a e 1",
      "5 b f 1",
      "6 c e 1",
      "7 d f 1",
      "8 a e 1",
      "9 b f 1",
      "10 c e 1",
      "11 d f 1"
    )
    val drt = new Derive_tool()
    val appRdd = sc.parallelize(arr)
    val appDf = appRdd
      .map(_.split(" "))
      .map(item => Data(item(0).toInt, item(1), item(2), item(3).toInt))
      .toDF()





  }
}
