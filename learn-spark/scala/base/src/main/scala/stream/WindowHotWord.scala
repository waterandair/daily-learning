package stream

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

// 热点搜索词滑动统计，每隔10秒钟，统计最近60秒钟的搜索词的搜索频次，并打印出排名最靠前的3个搜索词以及出现次数
object WindowHotWord {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local[2]")
      .setAppName("WindowHotWord")
    val ssc = new StreamingContext(conf, Seconds(1))
    val searchLogsDStream = ssc.socketTextStream("localhost", 9999)

    // 格式 name word
    val searchWordsDStream = searchLogsDStream.map(_.split(" ")(1))
    val searchWordPairsDStream = searchWordsDStream.map( searchWord => (searchWord, 1))
    val searchWordCountsDStream = searchWordPairsDStream.reduceByKeyAndWindow(
      (v1: Int, v2:Int) => v1 + v2,
      Seconds(60),  // 窗口长度
      Seconds(10)   // 滑动间隔
    )

    val finalDStream = searchWordCountsDStream.transform(searchWordCountsRDD => {
      val countSearchWordRDD = searchWordCountsRDD.map(tuple => (tuple._2, tuple._1))
      val sortedCountSearchWordsRDD = countSearchWordRDD.sortByKey(ascending = false)
      val sortedSearchWordCountsRDD = sortedCountSearchWordsRDD.map(tuple => (tuple._2, tuple._1))
      val top3SearchWordCounts = sortedSearchWordCountsRDD.take(3)

      for(tuple <- top3SearchWordCounts) {
        println("----- " + tuple)
      }

      searchWordCountsRDD
    })

    // 触发 job 执行
    finalDStream.print()

    ssc.start()
    ssc.awaitTermination()
  }
}
