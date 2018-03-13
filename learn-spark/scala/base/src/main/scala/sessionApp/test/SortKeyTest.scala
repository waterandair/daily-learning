package sessionApp.test

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

object SortKeyTest {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("SortKeyTest")

    val sc = new SparkContext(conf)

    val arr = Array(Tuple2(new SortKey(30, 35, 40), "1"),
      Tuple2(new SortKey(35, 30, 40), "2"),
      Tuple2(new SortKey(30, 38, 30), "3"))

    val rdd = sc.parallelize(arr, 1)

    val sortedRdd = rdd.sortByKey()

    for(tuple <- sortedRdd.collect()) {
      println(tuple._2)
    }
  }
}
