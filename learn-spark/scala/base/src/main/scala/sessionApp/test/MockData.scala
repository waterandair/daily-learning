package sessionApp.test

import java.util.UUID

import org.apache.spark.SparkContext
import org.apache.spark.sql.types._
import org.apache.spark.sql.{DataFrame, Row, RowFactory, SparkSession}
import sessionApp.utils.{DateUtils, StringUtils}

import scala.collection.mutable.ArrayBuffer
import scala.util.Random

class MockData

object MockData{
  def mock(sc:SparkContext, sparkSession:SparkSession): Unit ={
    val rows = ArrayBuffer[Row]()

    val searchKeywords = Array("火锅", "蛋糕", "重庆辣子鸡", "重庆小面",
      "呷哺呷哺", "新辣道鱼火锅", "国贸大厦", "太古商场", "日本料理", "温泉")

    /**
      *  user_visit_action(Hive 表)
      */
    // 日期,代表这个用户点击行为是在那一天发生的
    val date = DateUtils.getTodayDate()
    val actions = Array("search", "click", "order", "pay")
    val random = new Random()

    for(i <- 0 until 100){
      // 代表这个点击行为是哪一个用户执行的
      val userid: Long = random.nextInt(100).toLong

      for (j <- 0 until 10){
        // 唯一标示了某个用户的一个访问session
        val sessionId = UUID.randomUUID().toString.replace("-", "")
        val baseActionTime = date + " " + random.nextInt(23)

        for(k <- 0 until random.nextInt(100)){
          // 点击了某些商品/品类,也可能是搜索了某个关键词,然后进入了某个页面,页面的id
          val pageId = random.nextInt(10).toLong
          // 这个点击行为发生的时间点
          val actionTime = baseActionTime + ":" +
            StringUtils.fulfuill(random.nextInt(59).toString) + ":" +
            StringUtils.fulfuill(random.nextInt(59).toString)
          // 如果用户执行的是一个搜索行为,关键词
          var searchKeyWord:String = null
          // 可能是在网站首页,点击了某个品类 (美食,电子设备,电脑)
          var clickCategoryId: Long = 0L
          // 可能是再网站首页或者商品列表,点击了某个商品,商品id
          var clickProductId: Long = 0L
          // 代表了可能将某些商品加入了购物车,然后一次性下单,这就代表了某次下单行为中,有那些商品品类
          // 可能有 6 个商品,但是对应了两个 品类
          var orderCategoryIds: String = null
          // 某次下单,具体对那些商品下的订单
          var orderProductIds: String = null
          // 代表的是对某个订单,或者某几个订单,进行了一次支付的行为,对应了那些品类
          var payCategoryIds: String = null
          // 代表了某次支付行为中对应的商品的id
          var payProductIds: String = null
          var action = actions(random.nextInt(4))

          action match{
            case "search" => searchKeyWord = searchKeywords(random.nextInt(10))
            case "click" =>
              clickCategoryId = random.nextInt(100).toLong
              clickProductId = random.nextInt(100).toLong
            case "order" =>
              orderCategoryIds = random.nextInt(100).toString
              orderProductIds = random.nextInt(100).toString
            case "pay" =>
              payCategoryIds = random.nextInt(100).toString
              payProductIds = random.nextInt(100).toString

          }

          // To create a new Row, use [[RowFactory.create()]] in Java or [[Row.apply()]] in Scala.
          val row: Row = Row.apply(date, userid, sessionId,
            pageId, actionTime, searchKeyWord, clickCategoryId, clickProductId,
            orderCategoryIds, orderProductIds, payCategoryIds, payProductIds)
          rows.append(row)
          }

        }
    }

    val rowsRDD = sc.parallelize(rows)
    val schema = StructType(
      Array(
        StructField("date", StringType, true),
        StructField("user_id",LongType, true),
        StructField("session_id", StringType, true),
        StructField("page_id", LongType, true),
        StructField("action_time", StringType, true),
        StructField("search_keyword", StringType, true),
        StructField("click_category_id", LongType, true),
        StructField("click_product_id", LongType, true),
        StructField("order_category_ids", StringType, true),
        StructField("order_product_ids", StringType, true),
        StructField("pay_category_ids", StringType, true),
        StructField("pay_product_ids", StringType, true)
      )
    )
    val df: DataFrame = sparkSession.createDataFrame(rowsRDD, schema)
    df.createOrReplaceTempView("user_visit_action")
    sparkSession.sql("select * from user_visit_action").show()

    /**********************************************/
    rows.clear()
    val sexes = Array("male", "feamle")
    for(i <- 1 until 100){
      val userid = i.toLong
      val username = "user" + i.toString
      val name = "name" + i
      val age = random.nextInt(60)
      val professional = "professional" + random.nextInt(10)
      val city = "city" + random.nextInt(100)
      val sex = sexes(random.nextInt(2))
      val row: Row = Row.apply(userid, username, name, age, professional, city, sex)

      rows.append(row)
    }

    val rowsRDD2 = sc.parallelize(rows)
    val schema2 = StructType(Array(
      StructField("user_id", LongType, true),
      StructField("username", StringType, true),
      StructField("name", StringType, true),
      StructField("age", IntegerType, true),
      StructField("professional", StringType, true),
      StructField("city", StringType, true),
      StructField("sex", StringType, true)
    ))
    val df2 = sparkSession.createDataFrame(rowsRDD2, schema2)
    df2.createOrReplaceTempView("user_info")
    sparkSession.sql("select * from user_info").show()

  }

}
