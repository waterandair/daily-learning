package sql.newsOfflineStat

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SparkSession

object NewsOfflineStatSpark {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("NewsOfflineStatSpark")
    val sc = new SparkContext(conf)
    val spark =  SparkSession.builder() .config("spark.sql.warehouse.dir", "/user/hive/warehouse").enableHiveSupport().getOrCreate()

    // 使用 hive 关键字作为字段,需要用 反引号 引起来
    // create table news_access (`date` string,`timestamp` bigint,userid bigint,pageid bigint,section string,action string);
    //spark.sql("select * from news_access").show()
    spark.sql("select count(*) from news_access").show()

    /**
      * 实际场景中更多的情况是获取前一天的时期,进行计算
      */
    val yesterday = "2016-02-20"
    // pv
    //calculateDailyPagePv(spark, yesterday)
    // uv
    //calculateDailyPageUv(spark, yesterday)
    //calculateDailyNewUserRegisterRate(spark, yesterday)


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
              "date," +
              "pageid" +
      ") t " +
      "ORDER BY pv DESC"

    /**
      * 在这里，我们也可以转换成一个RDD，然后对RDD执行一个foreach算子,在foreach算子中，将数据写入mysql中
      */
    spark.sql(sql).show()
  }

  /**
    * 计算每个页面的每日 uv 并排序
    * spark sql 的 count(distinct) 语句,有bug, 默认会产生严重的数据倾斜,只会用一个task,去做去重和汇总计数,性能很差
    */
  def calculateDailyPageUv(spark: SparkSession, yesterday: String): Unit ={
    val sql = "SELECT date, pageid, uv FROM (" +
      "SELECT date, pageid, count(*) uv FROM (" +
            "SELECT date, pageid, userid FROM news_access WHERE date='" + yesterday + "' AND action='view' GROUP BY date, pageid, userid" +
        ") t2 GROUP BY date, pageid " +
      ") t ORDER BY uv DESC"

    spark.sql(sql).show()
  }

  /**
    * 计算每天新用户注册比例
    */
  def calculateDailyNewUserRegisterRate(spark:SparkSession, yesterday:String): Unit ={

    // 昨天所有访问行为中,userid 为 null, 新用户的访问总数
    val sql1 = "SELECT count(*) FROM news_access WHERE action='view' AND date='" + yesterday + "' AND userid IS NULL"
    // 昨天的总注册用户数
    val sql2 = "SELECT count(*) FROM news_access WHERE action='register' AND date='" + yesterday + "'"

    val res1 = spark.sql(sql1).collect()(0)(0).toString.toDouble
    val res2 = spark.sql(sql2).collect()(0)(0).toString.toDouble
    println(res1)
    println(res2)

    val res3 = res2 / res1
    println(res3.formatted("%.2f"))

  }

}
