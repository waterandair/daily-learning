package stream.kafka

import javax.lang.model.element.NestingKind

import kafka.serializer.StringDecoder
import org.apache.spark.SparkConf
import org.apache.spark.streaming.dstream.{DStream, SocketInputDStream}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.kafka._

object NewsRealtimeStatSpark {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local[2]")
      .setAppName("NewsRealtimeStatSpark")
    val ssc = new StreamingContext(conf, Seconds(5))

    val kafkaParams = Map[String, String]("metadata.broker.list" -> "localhost:9092")
    val topics = Set("news-access")

    val lines = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topics)

    // 过滤出访问日志
    val accessDStream = lines.filter(line =>{
      val log = line._2.split(" ")
      val action = log(5)
      if("view" == action) true else false
    })


    // 计算5秒内pv
    //calculatePagePV(accessDStream)

    // 计算5秒内uv
    calculatePageUv(accessDStream)


    ssc.start()
    ssc.awaitTermination()
  }

  /**
    * 计算 pv
    */
  def calculatePagePV(accessDStream: DStream[(String,String)]): Unit ={
    val pageidDStream = accessDStream.map(tuple => {
      val log = tuple._2
      val logSplit = log.split(" ")
      val pageid = logSplit(3)
      (pageid, 1L)
    })

    // 计算出每十秒的页面 pv 之后,真实场景中,应该持久化,到mysql 或 redis 中,对每个页面的pv 进行累加
    // 其他应用就可以从 mysql 和 redis 中,读取page pv 实时变化的数据,以及曲线图
    val pagePvDStream = pageidDStream.reduceByKey(_ + _)
    pagePvDStream.print()

  }

  // 计算页面 uv
  def calculatePageUv(accessDStream: DStream[(String,String)]): Unit ={
    val pageidUseridDStream = accessDStream.map(tuple => {
      val log = tuple._2
      val logSplited = log.split(" ")
      val pageid = logSplited(3)
      val userid = logSplited(2)
      pageid + "_" + userid
    })

    val distinctPageidUseridDStream = pageidUseridDStream.transform(_.distinct())

    val pageidDSTREAM = distinctPageidUseridDStream.map(pageid_userid => {
      val  pageid = pageid_userid.split("_")(0)
      (pageid, 1)
    })

    val uv = pageidDSTREAM.reduceByKey(_ + _)
    uv.print()
  }
}
