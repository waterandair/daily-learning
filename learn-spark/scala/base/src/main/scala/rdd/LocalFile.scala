package rdd

import org.apache.spark.{SparkConf, SparkContext}

object LocalFile {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("LocalFile").setMaster("local")
    val sc = new SparkContext(conf)

    val lines = sc.textFile("/usr/local/spark-2.2.1/README.md")
    val count = lines.map(line => line.length).reduce(_ + _)

    println("file's count is " + count )
  }
}
