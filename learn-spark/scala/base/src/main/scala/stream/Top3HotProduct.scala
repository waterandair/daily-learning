package stream

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.sql.{Row, SparkSession}

object Top3HotProduct {

  case class HotProduct(category: String, product: String, click_count: Long)
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local[2]")
      .setAppName("Top3HotProduct")
    val ssc = new StreamingContext(conf, Seconds(10))

    val productClickLogsDStream = ssc.socketTextStream("localhost", 9999)
    // 输入格式  customer product category
    val categoryProductPairsDStream = productClickLogsDStream
      .map(productClickLog => (productClickLog.split(" ")(2) + "_" + productClickLog.split(" ")(1), 1))

    // 每十秒计算一次最近60内每种商品的数量
    val categoryProductCountsDStream = categoryProductPairsDStream.reduceByKeyAndWindow(
      (v1: Int, v2:Int) => v1 + v2,
      Seconds(60),
      Seconds(10)
    )

    // DStream 转换为 RDD 然后再用反射的方式转为 DF
    categoryProductCountsDStream.foreachRDD(categoryProductCountsRDD => {
      val spark = SparkSession.builder().config(categoryProductCountsRDD.sparkContext.getConf).getOrCreate()
      import spark.implicits._

      val categoryProductCountDF = categoryProductCountsRDD.map(tuple => {
       HotProduct(tuple._1.split("_")(0), tuple._1.split("_")(1), tuple._2.toInt)
      }).toDF()

      categoryProductCountDF.createOrReplaceTempView("product_click_log")

      val top3ProductDF = spark.sql(
        "SELECT category,product,click_count "
          + "FROM ("
          + "SELECT "
          + "category,"
          + "product,"
          + "click_count,"
          + "row_number() OVER (PARTITION BY category ORDER BY click_count DESC) rank "
          + "FROM product_click_log"
          + ") tmp "
          + "WHERE rank<=3")

      top3ProductDF.show()
    })

    ssc.start()
    ssc.awaitTermination()
  }
}
