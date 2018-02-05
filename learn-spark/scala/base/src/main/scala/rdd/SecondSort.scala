package rdd

import org.apache.spark.{SparkConf, SparkContext}

/**
  * 二次排序
  */
object SecondSort {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName("SecondSort")
      .setMaster("local")
    val sc= new SparkContext(conf)

    val linesArr = Array("1 5", "2 4", "3 6", "1 3", "2 1")
    val lines = sc.parallelize(linesArr)

    val sort = lines.map(line => (
        new SecondSortKey(line.split(" ")(0).toInt, line.split(" ")(1).toInt),
        line
      )
    )

    val sorted = sort.sortByKey()
    val sortedLines = sorted.map(_._2)

    sortedLines.foreach(println)
  }
}
