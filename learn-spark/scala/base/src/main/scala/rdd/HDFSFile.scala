package rdd

import org.apache.spark.{SparkConf, SparkContext}

object HDFSFile {

  def main(args: Array[String]) {
    val conf = new SparkConf().setAppName("hdfsFile").setMaster("local[4]") ;
    val sc = new SparkContext(conf)

    val lines = sc.textFile("hdfs://127.0.0.1:9000/user/zj/spark/base/README.md", 1)
    val count = lines.map { line => line.length() }.reduce(_ + _)

    println("file's count is " + count)
  }
}