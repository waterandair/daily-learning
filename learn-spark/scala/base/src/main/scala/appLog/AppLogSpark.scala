package appLog

import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

object AppLogSpark {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName("AppLogSpark")
      .setMaster("local")

    val sc = new SparkContext(conf)

    // 读取日志文件,并创建一个 rdd
    // 格式: 时间戳 设备id 上行流量 下行流量
    val accessLogRDD = sc.textFile("hdfs://localhost:9000/user/zj/spark/access.log")

    // 将 rdd 映射为 key-value 格式,为后面的 reduceByKey 聚合做准备
    val accesslogPairRDD = mapAccessLogRDD2Pair(accessLogRDD)
    //accesslogPairRDD.foreach(println(_))

    // 根据 deviceID 进行聚合操作
    // 获取每个 deviceID 的中上行流量,总下行流量,最早访问时间戳
    val aggrAccessLogPairRDD = aggregateByDeviceId(accesslogPairRDD)

    /*aggrAccessLogPairRDD.foreach(value => {
      println(value._1)
      println(value._2.timestamps + " " + value._2.upTraffics + " " + value._2.downTraffics)
    })*/

    val accessSortRDD = mapRDDKey2SortKey(aggrAccessLogPairRDD)
    val top10AccessSortRDD = accessSortRDD.take(10)
    top10AccessSortRDD.foreach(value => {
      println(value._1)
      println(value._2.timestamps + " " + value._2.upTraffics + " " + value._2.downTraffics)
    })

  }

  /**
    * 将日志 RDD 映射为 key-value 的格式
    * accessLogRDD 日志格式
    * @param accessLogRDD
    */
  def mapAccessLogRDD2Pair(accessLogRDD: RDD[String]): RDD[Tuple2[String, AccessLogInfo]] ={
    val res = accessLogRDD.map(accessLog => {
      // 根据 /t 对日志进行切分
      val accessLogSplited = accessLog.split("\t")

      // 获取四个字段
      val timestamp = accessLogSplited(0).toLong
      val deviceID:String = accessLogSplited(1).toString
      val upTraffic = accessLogSplited(2).toInt
      val downTraffic = accessLogSplited(3).toInt

      // 将时间戳,上行流量,下行流量,封装为自定义的可序列化对象
      val accessLogInfo: AccessLogInfo = new AccessLogInfo(timestamp, upTraffic, downTraffic)
      (deviceID, accessLogInfo)
    })

    res
  }

  /**
    * 根据 deviceID 进行聚合操作
    * 计算出每个 deviceID 的总上行流量,总下行流量以及最早访问时间
    */
  def aggregateByDeviceId(accessLogPairRDD:RDD[Tuple2[String, AccessLogInfo]])={
    val res = accessLogPairRDD.reduceByKey((log1, log2) => {
      val timestamp = if (log1.timestamps < log2.timestamps) {
        log1.timestamps
      } else{
        log2.timestamps
      }

      val upTraffic = log1.upTraffics + log2.upTraffics
      val downTraffic = log1.downTraffics + log2.downTraffics

      val accessLogInfo = new AccessLogInfo(timestamp, upTraffic, downTraffic)
      accessLogInfo
    })
    res
  }

  /**
    * 将 RDD 的 key 映射为 二次排序的 key
    */
  def mapRDDKey2SortKey(aggrAccessLogPairRDD: RDD[Tuple2[String, AccessLogInfo]]) = {
    val sortKey = aggrAccessLogPairRDD.map(line => (
      new AccessSortKey(line._2.upTraffics, line._2.downTraffics),
      line
      ))

    val sorted = sortKey.sortByKey(false)
    val sortedLines = sorted.map(_._2)
    sortedLines
  }
}
