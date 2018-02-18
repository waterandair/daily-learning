package stream.flume

import org.apache.spark.SparkConf
import org.apache.spark.streaming.flume.FlumeUtils
import org.apache.spark.streaming.flume._
import org.apache.spark.streaming.{Seconds, StreamingContext}

//一定要先启动flume，再启动spark streaming
object FlumePollWordCount {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local[3]")
      .setAppName("FlumePollWordCount")
    val ssc = new StreamingContext(conf, Seconds(5))

    val lines = FlumeUtils.createPollingStream(ssc, "127.0.0.1", 8888)

    val wordCount = lines
      .flatMap(line => {
        val res = new String(line.event.getBody.array())
        res.split(" ")
      })
      .map((_, 1))
      .reduceByKey(_ + _)

    wordCount.print()

    ssc.start()
    ssc.awaitTermination()

  }
}
