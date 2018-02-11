package rdd

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

object ParallelizeCollection {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("ParallelizeCollection").setMaster("local")
    val sc = new SparkContext(conf)

    val numbers = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val numberRdd = sc.parallelize(numbers, 3)
    val sum = numberRdd.reduce(_ + _)

    println("累加和: " + sum)
  }
}