package stream

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}



object Wordcount {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("Wordcount")

    var ssc = new StreamingContext(conf, Seconds(1))

    val lines = ssc.socketTextStream("localhost", 9999)
    val wordcount = lines.flatMap(_.split(" "))
      .map(word => (word, 1))
      .reduceByKey(_ + _)

    Thread.sleep(5000)
    wordcount.print()

    ssc.start()
    ssc.awaitTermination()
  }
}
