package newsOfflineStat

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SparkSession

object NewsOfflineStatSpark {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("NewsOfflineStatSpark")
    val sc = new SparkContext(conf)
    val spark =  SparkSession.builder().enableHiveSupport().getOrCreate()

    //spark.sql("select * from news_access").show()

    /**
      * 实际场景中更多的情况是获取前一天的时期,进行计算
      */
    val yesterday = "2016-02-20"
    calculateDailyPagePv(spark, yesterday)




  }


  /**
    * 页面 pv 统计以及排序
    * 排序后，插入mysql，java web系统要查询每天pv top10的页面，直接查询mysql表limit 10就可以
    *   如果我们这里不排序，那么web系统就要做排序，反而会影响java web系统的性能，以及用户响应时间
    */
  def calculateDailyPagePv(spark: SparkSession, yesterday: String): Unit ={
    /**
      * 注意: select后面的非聚合列必须出现在group by中，否则非法
      */
    val sql = "SELECT " +
      "date, " +
      "pageid, " +
      "pv " +
      "FROM (" +
        "SELECT " +
          "date ," +
          "pageid, " +
          "count(*) pv " +
        "FROM " +
          "news_access " +
            "WHERE " +
              "action='view'" +
              " AND " +
              "date='" + yesterday + "'" +
              " GROUP " +
              "BY " +
              "date" +
              "pageid" +
      ") t " +
      "ORDER BY pv DESC"

    /**
      * 在这里，我们也可以转换成一个RDD，然后对RDD执行一个foreach算子,在foreach算子中，将数据写入mysql中
      */
    spark.sql(sql).show()
  }

  /**
    *
    */
  def calculateDailyPageUv(spark: SparkSession, yesterday: String): Unit ={

  }
}
