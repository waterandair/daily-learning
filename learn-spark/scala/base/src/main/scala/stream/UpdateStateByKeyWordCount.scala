package stream

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

object UpdateStateByKeyWordCount {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local[2]")
      .setAppName("UpdateStateByKeyWordCount")

    val ssc = new StreamingContext(conf, Seconds(5))
    ssc.checkpoint("hdfs://localhost:9000/user/zj/spark/wordcount_checkpoint")

    val lines = ssc.socketTextStream("localhost", 9999)
    val words = lines.flatMap(_.split(" "))
    val pairs = words.map(word => (word, 1))
    val wordCount = pairs.updateStateByKey((values: Seq[Int], state: Option[Int]) => {
      var newValue = state.getOrElse(0)
      for (value <- values) {
        println(value)
        newValue += value
      }

      Option(newValue)
    })

    wordCount.print()

    ssc.start()
    ssc.awaitTermination()
  }
}
