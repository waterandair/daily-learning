package stream

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

object TransformBlacklist {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local[2]")
      .setAppName("TransformBlacklist")
    val ssc = new StreamingContext(conf, Seconds(5))

    val blacklist = Array(
      ("tom", true)
    )
    // 模拟一个黑名单
    val blacklistRDD = ssc.sparkContext.parallelize(blacklist, 5)

    // 输入数据格式为(date, name)
    val adsClickLogStream = ssc.socketTextStream("localhost", 9999)
    // 转换为 (name, (date, name)) 格式
    val userAdsClickLogStream = adsClickLogStream
      .map( adsClickLog => (adsClickLog.split(" ")(1), adsClickLog))

    val validAdsClickLogDStream = userAdsClickLogStream.transform( userAdsClickLogRDD => {

      // 转换为 (name, ((date, name), true)) 的格式
      val joinedRDD = userAdsClickLogRDD.leftOuterJoin(blacklistRDD)
      val filteredRDD = joinedRDD.filter(tuple => {
        if(tuple._2._2.getOrElse(false)){
          false
        } else {
          true
        }
      })

      val validAdsClickLogRDD = filteredRDD.map(tuple => tuple._2._1)
      validAdsClickLogRDD
    })

    validAdsClickLogDStream.print()
    ssc.start()
    ssc.awaitTermination()

  }
}
