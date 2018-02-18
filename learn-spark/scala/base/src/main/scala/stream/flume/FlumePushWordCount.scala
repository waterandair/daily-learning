package stream.flume

import org.apache.spark.SparkConf
import org.apache.spark.streaming.flume.FlumeUtils
import org.apache.spark.streaming.{Seconds, StreamingContext}

object FlumePushWordCount {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName("FlumePushWordCount")
      .setMaster("local[2]")
    val ssc = new StreamingContext(conf,Seconds(5))

    val lines = FlumeUtils.createStream(ssc, "127.0.0.1", 8888)

    val wordCount = lines
      .flatMap(event => {
        val line = new String(event.event.getBody.array()).split(" ")
        line
      })
      .map(word => (word, 1))
      .reduceByKey(_ + _)

    wordCount.print()

    ssc.start()
    ssc.awaitTermination()


  }
}
