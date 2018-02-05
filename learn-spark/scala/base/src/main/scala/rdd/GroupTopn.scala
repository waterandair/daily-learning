package rdd

import org.apache.spark.{SparkConf, SparkContext}

object GroupTopn {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName("GroupTopn")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val scores = Array(
      "class1 90",
      //"class2 56",
      "class1 87",
      "class1 76",
      //"class2 88",
      "class1 95",
      "class1 74",
      //"class2 87",
      "class2 67",
      "class2 77"
    )
    val scoresRdd = sc.parallelize(scores)

    val sortScoresRdd = scoresRdd.map(line => (line.split(" ")(1), line.split(" ")(0))).sortByKey(ascending = false)
    val groupRdd = sortScoresRdd.map(scores => (scores._2, scores._1)).groupByKey()
    groupRdd.foreach(groupRdd => {
      println(groupRdd._1)
      val len = groupRdd._2.size
      var scores: Iterable[Any] = scala.collection.mutable.ArrayBuffer()
      if (len >= 3) {
        scores = groupRdd._2.take(3)
      } else {
        scores = groupRdd._2.take(len)
      }

      scores.foreach(score => println("---" + score))
    })
  }
}
