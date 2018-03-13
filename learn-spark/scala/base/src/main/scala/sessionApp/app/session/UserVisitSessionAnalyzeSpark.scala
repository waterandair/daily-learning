package sessionApp.app.session

import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}
import com.alibaba.fastjson.{JSON, JSONObject}
import org.apache.spark.rdd.RDD
import sessionApp.conf.ConfigurationManager
import sessionApp.constant.Constant
import sessionApp.factory.DAOFactory
import sessionApp.test.MockData
import sessionApp.utils.{DateUtils, NumberUtils, ParamUtils, StringUtils, ValidUtils}
import sessionApp.domain.SessionAggrStat

import scala.collection.mutable.ArrayBuffer
import java.util.Date

import scala.util.Random
/**
  * 用户访问 session 分析
  *
  * 接收用户创建的分析任务，用户可能指定的条件如下：
  * 1、时间范围：起始日期~结束日期
  * 2、性别：男或女
  * 3、年龄范围
  * 4、职业：多选
  * 5、城市：多选
  * 6、搜索词：多个搜索词，只要某个session中的任何一个action搜索过指定的关键词，那么session就符合条件
  * 7、点击品类：多个品类，只要某个session中的任何一个action点击过某个品类，那么session就符合条件
  */
object UserVisitSessionAnalyzeSpark {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName(Constant.SPARK_APP_NAME_SESSION)
      .setMaster("local")
    val sc = new SparkContext(conf)
    val sparkSession = SparkSession
      .builder()
      .getOrCreate()

    // 生成模拟数据
    mockData(sc, sparkSession)

    // 创建需要使用的DAO组件
    val taskDao = DAOFactory.getTaskDAO()

    // 查询出指定的任务
    val taskid = ParamUtils.getTaskIdFromArgs(args, Constant.SPARK_LOCAL_TASKID_SESSION)

    val task = taskDao.findById(taskid)
    val taskParam: JSONObject = JSON.parseObject(task.getString("task_param"))

    /**
      * 1. 如果要进行 session 粒度的数据聚合
      * 首先要从 user_visit_action 表中,查询出来指定日期内的行为数据
      */
    val actionRDD = getActionRDDByDateRange(sparkSession, taskParam)

    /**
      * 2. 可以将行为数据, 按照session_id 进行 group_by 分组,此时的数据的粒度就是 session 粒度了,然后,将session 粒度的数据与用户
      * 信息数据,进行join,然后就可以获取到 session 粒度的数据,同时还包含了 session 对应的 user 信息
      */
    val session2AggrInfoRDD = aggregateBySession(sparkSession, actionRDD)
    //session2AggrInfoRDD.foreach(line => println(line))

    /**
      * 3. 针对 session 粒度的聚合数据,按照使用者指定的筛选参数进行数据过滤
      */
    // 注册一个自定义累加器
    val sessionAggrStatAccumulator = new SessionAggrStatAccumulator
    sc.register(sessionAggrStatAccumulator, "sessionAggrStatAccumulator")

    val filteredSessioniid2AggrInfoRDD = filteredSessionid2AggrStat(session2AggrInfoRDD, taskParam, sessionAggrStatAccumulator)

    println(filteredSessioniid2AggrInfoRDD.count())



    /**
      * 从Accumulator中，获取数据，插入数据库的时候，一定要，一定要，是在有某一个action操作以后
      * 再进行。。。
      * 如果没有action的话，那么整个程序根本不会运行。。。
      */
    // 计算出各个范围的session占比，并写入MySQL
    calculateAndPersistAggrStat(sessionAggrStatAccumulator.value, taskid.toString)

    /**
      * session聚合统计（统计出访问时长和访问步长，各个区间的session数量占总session数量的比例）
      *
      * 如果不进行重构，直接来实现，思路：
      * 1、actionRDD，映射成<sessionid,Row>的格式
      * 2、按sessionid聚合，计算出每个session的访问时长和访问步长，生成一个新的RDD
      * 3、遍历新生成的RDD，将每个session的访问时长和访问步长，去更新自定义Accumulator中的对应的值
      * 4、使用自定义Accumulator中的统计值，去计算各个区间的比例
      * 5、将最后计算出来的结果，写入MySQL对应的表中
      *
      * 普通实现思路的问题：
      * 1、为什么还要用actionRDD，去映射？其实我们之前在session聚合的时候，映射已经做过了。多此一举
      * 2、是不是一定要，为了session的聚合这个功能，单独去遍历一遍session？其实没有必要，已经有session数据
      * 		之前过滤session的时候，其实，就相当于，是在遍历session，那么这里就没有必要再过滤一遍了
      *
      * 重构实现思路：
      * 1、不要去生成任何新的RDD（处理上亿的数据）
      * 2、不要去单独遍历一遍session的数据（处理上千万的数据）
      * 3、可以在进行session聚合的时候，就直接计算出来每个session的访问时长和访问步长
      * 4、在进行过滤的时候，本来就要遍历所有的聚合session信息，此时，就可以在某个session通过筛选条件后
      * 		将其访问时长和访问步长，累加到自定义的Accumulator上面去
      * 5、就是两种截然不同的思考方式，和实现方式，在面对上亿，上千万数据的时候，甚至可以节省时间长达
      * 		半个小时，或者数个小时
      *
      * 开发Spark大型复杂项目的一些经验准则：
      * 1、尽量少生成RDD
      * 2、尽量少对RDD进行算子操作，如果有可能，尽量在一个算子里面，实现多个需要做的功能
      * 3、尽量少对RDD进行shuffle算子操作，比如groupByKey、reduceByKey、sortByKey（map、mapToPair）
      * 		shuffle操作，会导致大量的磁盘读写，严重降低性能
      * 		有shuffle的算子，和没有shuffle的算子，甚至性能，会达到几十分钟，甚至数个小时的差别
      * 		有shfufle的算子，很容易导致数据倾斜，一旦数据倾斜，简直就是性能杀手（完整的解决方案）
      * 4、无论做什么功能，性能第一
      * 		在传统的J2EE或者.NET后者PHP，软件/系统/网站开发中，我认为是架构和可维护性，可扩展性的重要
      * 		程度，远远高于了性能，大量的分布式的架构，设计模式，代码的划分，类的划分（高并发网站除外）
      *
      * 		在大数据项目中，比如MapReduce、Hive、Spark、Storm，我认为性能的重要程度，远远大于一些代码
      * 		的规范，和设计模式，代码的划分，类的划分；大数据，大数据，最重要的，就是性能
      * 		主要就是因为大数据以及大数据项目的特点，决定了，大数据的程序和项目的速度，都比较慢
      * 		如果不优先考虑性能的话，会导致一个大数据处理程序运行时间长度数个小时，甚至数十个小时
      * 		此时，对于用户体验，简直就是一场灾难
      *
      * 		所以，推荐大数据项目，在开发和代码的架构中，优先考虑性能；其次考虑功能代码的划分、解耦合
      *
      * 		我们如果采用第一种实现方案，那么其实就是代码划分（解耦合、可维护）优先，设计优先
      * 		如果采用第二种方案，那么其实就是性能优先
      *
      *
      */
  }

  /**
    * 生成模拟数据, 只有本地模式才会去生成模拟数据
    */
  def mockData(sc: SparkContext, sparkSession: SparkSession): Unit = {
    val local = ConfigurationManager.getProperty(Constant.SPARK_LOCAL).toBoolean
    if (local) {
      MockData.mock(sc, sparkSession)
    }
  }

  /**
    * actionRDD 就是一个公共rdd,
    *   1. 要用到 actionRDD, 获取到一个公共的 sessionid 为 key 的 pairRDD
    *   2. actionRDD, 用在了 session 聚合环节里面
    */
  def getActionRDDByDateRange(sparkSession: SparkSession, taskParams: JSONObject): RDD[Row] = {
    val startDate = ParamUtils.getParam(taskParams, Constant.PARAM_START_DATE)
    val endDate = ParamUtils.getParam(taskParams, Constant.PARAM_END_DATE)

    val sql = "select * from user_visit_action where date >='" + startDate + "' and date<='" + endDate + "'"
    val actionDF = sparkSession.sql(sql).rdd
    // TODO
    actionDF
  }

  /**
    * 对行为数据按照 session 粒度进行聚合
    */
  def aggregateBySession(sparkSession: SparkSession, actionRDD: RDD[Row]): RDD[(String, String)] = {
    // 现在 actionRDD 中的元素是Row, 一个 Row 就是一行用户访问行为的记录, 比如一次点击或者搜索
    // 要将这个 Row 映射成 <sessionid, ROW>
    val sessionid2ActionRDD = actionRDD.map(row => {
      (row.getString(2), row)
    })

    // 对行为数据按 session 进行分组
    val sessionid2ActionsRDD = sessionid2ActionRDD.groupByKey()
    // 对每一个 session 分组进行聚合, 将 session 中所有的搜索词和点击品类都聚合起来
    // 数据格式为 <userid, partAggrInfo(sessionid, searchkeywords,clickCategoryIds)>
    val userid2partAggrInfoRDD: RDD[Tuple2[Long, String]]= sessionid2ActionsRDD.map(row => {
      val sessionid = row._1
      val iterator = row._2.toIterator
      val searchKeywordsArray = ArrayBuffer[String]()
      val clickCategoryIdsArray = ArrayBuffer[String]()

      var userid: Long = 0L
      /**
        *
        */
      // session 的起始时间和结束时间
      var startTime: Date = null
      var endTime: Date = null
      // session 的访问步长
      var stepLength = 0

      // 遍历 session 所有的访问行为
      while (iterator.hasNext) {
        // 提取每个访问行为的搜索词字段和点击品类字段
        val row = iterator.next()
        if (userid == 0L) {
          userid = row.getLong(1)
        }
        //todo
        val searchKeyword = row.getString(5)
        val clickCategoryId = row.getLong(6)

        /**
          * 并不是每一行数据都有 searchKeyword 和 clickCategoryId, 所以数据可能出现null
          * 不能是null值
          */
        if (StringUtils.isNotEmpty(searchKeyword)) {
          if (searchKeywordsArray.indexOf(searchKeyword) == -1) {
            searchKeywordsArray.append(searchKeyword)
          }
        }
        if (clickCategoryId != 0L) {
          if (clickCategoryIdsArray.indexOf(clickCategoryId) == -1) {
            clickCategoryIdsArray.append(clickCategoryId.toString)
          }
        }

        // 计算 session 开始和结束时间
        val actionTime = DateUtils.parseTime(row.getString(4))

        if(startTime == null) {
          startTime = actionTime
        }
        if(endTime == null) {
          endTime = actionTime
        }

        if(actionTime.before(startTime)){
          startTime = actionTime
        }
        if(actionTime.after(endTime)) {
          endTime = actionTime
        }

        stepLength += 1

      }

      val searchKeyWords = searchKeywordsArray.toString()
      val clickCategoryIds = clickCategoryIdsArray.toString()
      // 计算 session 访问时长(秒)
      val visitLength = (endTime.getTime - startTime.getTime) / 1000

      val partAggrInfo = Constant.FIELD_SESSION_ID + "=" + sessionid + "|" +
        Constant.FIELD_SEARCH_KEYWORDS + "=" + searchKeyWords + "|" +
        Constant.FIELD_CLICK_CATEGORY_IDS + "=" + clickCategoryIds + "|" +
        Constant.FIELD_VISIT_LENGTH + "=" + visitLength + "|" +
        Constant.FIELD_STEP_LENGTH + "=" + stepLength

      (userid, partAggrInfo)
    })

//    println("userid2partAggrInfoRDD")
//    userid2partAggrInfoRDD.take(10).foreach(line => println(line._1))

    // 查询所有用户数据,并映射成<userid, row>
    val sql = "select * from user_info"
    val userInfoRDD = sparkSession.sql(sql).rdd
    val userid2InfoRDD = userInfoRDD.map(row => {
      (row.getLong(0), row)
    })

//    println("userid2InfoRDD")
//    userid2InfoRDD.take(10).foreach(line => println(line._1))

    // 将 session 粒度聚合数据,与用户信息进行join
    val userid2FullInfoRDD = userid2partAggrInfoRDD.join(userid2InfoRDD)
//    println("userid2FullInfoRDD -> " + userid2FullInfoRDD.count())

    // 将 join 起来的数据进行拼接,并且返回<sessionid, fullAggrInfo> 格式的数据
    val sessionid2FullAggrInfoRDD = userid2FullInfoRDD.map(row => {
      val partAggrInfo = row._2._1
      val userInfo = row._2._2
      val sessionid = StringUtils.getFieldFromConcatString(partAggrInfo, "\\|", Constant.FIELD_SESSION_ID)

      val age = userInfo.getInt(3)
      val professional = userInfo.getString(4)
      val city = userInfo.getString(5)
      val sex = userInfo.getString(6)

      val fullAggrInfo = partAggrInfo + "|" +
        Constant.FIELD_AGE + "=" + age + "|" +
        Constant.FIELD_PROFESSIONAL + "=" + professional + "|" +
        Constant.FIELD_CITY + "=" + city + "|" +
        Constant.FIELD_SEX + "=" + sex

      (sessionid, fullAggrInfo)
    })

    sessionid2FullAggrInfoRDD
  }

  /**
    * 根据筛选条件筛选 RDD
    */
  def filteredSessionid2AggrStat(sessionid2AggrInfoRDD:RDD[(String,String)],
                                 taskParam: JSONObject,
                                 sessionAggrStatAccumulator: SessionAggrStatAccumulator):RDD[(String, String)] ={
    val startAge = ParamUtils.getParam(taskParam, Constant.PARAM_START_AGE)
    val endAge = ParamUtils.getParam(taskParam, Constant.PARAM_END_AGE)
    val professionals = ParamUtils.getParam(taskParam, Constant.PARAM_PROFESSIONALS)
    val cities = ParamUtils.getParam(taskParam, Constant.PARAM_CITIES)
    val sex = ParamUtils.getParam(taskParam, Constant.PARAM_SEX)
    val keywords = ParamUtils.getParam(taskParam, Constant.PARAM_KEYWORDS)
    val categoryIds = ParamUtils.getParam(taskParam, Constant.PARAM_CATEGORY_IDS)

    var _parameter = (if(startAge != null)Constant.PARAM_START_AGE + "=" + startAge + "|"else "") +
      (if(endAge != null)Constant.PARAM_END_AGE + "=" + endAge + "|" else "") +
      (if(professionals != null)Constant.PARAM_PROFESSIONALS + "=" + professionals + "|" else "") +
      (if(cities != null)Constant.PARAM_CITIES + "=" + cities + "|" else "") +
      (if(sex != null)Constant.PARAM_SEX + "=" + sex + "|" else "") +
      (if(keywords != null)Constant.PARAM_KEYWORDS + "=" + keywords + "|" else "") +
      (if(categoryIds != null)Constant.PARAM_CATEGORY_IDS + "=" + categoryIds + "|" else "")

    if(_parameter.endsWith("|")){
      _parameter.substring(0, _parameter.length -1)
    }

    val parameter = _parameter

    /**
      * 计算访问时长范围
      * @param visitLength
      */
    def calculateVisitLength(visitLength: Long): Unit = {
      if(visitLength >=1 && visitLength <= 3) {
        sessionAggrStatAccumulator.add(Constant.TIME_PERIOD_1s_3s)
      } else if(visitLength >=4 && visitLength <= 6) {
        sessionAggrStatAccumulator.add(Constant.TIME_PERIOD_4s_6s)
      } else if(visitLength >=7 && visitLength <= 9) {
        sessionAggrStatAccumulator.add(Constant.TIME_PERIOD_7s_9s)
      } else if(visitLength >=10 && visitLength <= 30) {
        sessionAggrStatAccumulator.add(Constant.TIME_PERIOD_10s_30s)
      } else if(visitLength > 30 && visitLength <= 60) {
        sessionAggrStatAccumulator.add(Constant.TIME_PERIOD_30s_60s)
      } else if(visitLength > 60 && visitLength <= 180) {
        sessionAggrStatAccumulator.add(Constant.TIME_PERIOD_1m_3m)
      } else if(visitLength > 180 && visitLength <= 600) {
        sessionAggrStatAccumulator.add(Constant.TIME_PERIOD_3m_10m)
      } else if(visitLength > 600 && visitLength <= 1800) {
        sessionAggrStatAccumulator.add(Constant.TIME_PERIOD_10m_30m)
      } else if(visitLength > 1800) {
        sessionAggrStatAccumulator.add(Constant.TIME_PERIOD_30m)
      }
    }

    /**
      * 计算访问步长范围
      * @param stepLength
      */
    def calculateStepLength(stepLength: Long): Unit ={
      if(stepLength >= 1 && stepLength <= 3) {
        sessionAggrStatAccumulator.add(Constant.STEP_PERIOD_1_3)
      } else if(stepLength >= 4 && stepLength <= 6) {
        sessionAggrStatAccumulator.add(Constant.STEP_PERIOD_4_6)
      } else if(stepLength >= 7 && stepLength <= 9) {
        sessionAggrStatAccumulator.add(Constant.STEP_PERIOD_7_9)
      } else if(stepLength >= 10 && stepLength <= 30) {
        sessionAggrStatAccumulator.add(Constant.STEP_PERIOD_10_30)
      } else if(stepLength > 30 && stepLength <= 60) {
        sessionAggrStatAccumulator.add(Constant.STEP_PERIOD_30_60)
      } else if(stepLength > 60) {
        sessionAggrStatAccumulator.add(Constant.STEP_PERIOD_60)
      }
    }

    // 根据筛选参数进行过滤
    val filteredSessionid2AggrInfoRDD = sessionid2AggrInfoRDD.filter(row => {
      val aggrInfo = row._2
      var res = true

      // 按照年龄范围进行过滤(startAge, endAge)
      if (!ValidUtils.between(aggrInfo, Constant.FIELD_AGE, parameter, Constant.PARAM_START_AGE, Constant.PARAM_END_AGE)){
        res = false
      }

      // 按照职业范围进行过滤
      if (!ValidUtils.in(aggrInfo, Constant.FIELD_PROFESSIONAL, parameter, Constant.PARAM_PROFESSIONALS)) {
        res = false
      }

      // 按照城市范围过滤
      if (!ValidUtils.in(aggrInfo, Constant.FIELD_CITY, parameter, Constant.PARAM_CITIES)) {
        res = false
      }

      // 按照性别进行过滤
      if(!ValidUtils.equal(aggrInfo, Constant.FIELD_SEX, parameter, Constant.PARAM_SEX)) {
        res = false
      }

      // 按照搜索词进行过滤
      if (!ValidUtils.in(aggrInfo, Constant.FIELD_SEARCH_KEYWORDS, parameter, Constant.PARAM_KEYWORDS)) {
        res = false
      }

      // 按照点击品类id进行过滤
      if (!ValidUtils.in(aggrInfo, Constant.FIELD_CLICK_CATEGORY_IDS, parameter, Constant.PARAM_CATEGORY_IDS)) {
        res = false
      }

      // 过滤之后,这里可以对 session 的访问时长和访问步长进行统计, 根据 session 对应的范围,进行累加
      sessionAggrStatAccumulator.add(Constant.SESSION_COUNT)
      // 计算除 session 的访问时长和访问步长的范围,并进行相应的累加
      val visitLength = StringUtils.getFieldFromConcatString(aggrInfo, "\\|", Constant.FIELD_VISIT_LENGTH).toLong
      val stepLength = StringUtils.getFieldFromConcatString(aggrInfo, "\\|", Constant.FIELD_STEP_LENGTH).toLong

      calculateVisitLength(visitLength)
      calculateStepLength(stepLength)

      res
    })



    filteredSessionid2AggrInfoRDD
  }


  /**
    * 计算结果持久化
    * @param value
    * @param taskid
    */
  def calculateAndPersistAggrStat(value: String, taskid: String): Unit ={

    def toLong(s: String): Option[Long] = {
      try {
        Some(s.toLong)
      } catch {
        case e: Exception => None
      }
    }

    def show(x: Option[Long]):Long = x match {
      case Some(s) => s
      case None => 0L
    }

    val session_count: Long = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.SESSION_COUNT)))

    val visit_length_1s_3s: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.TIME_PERIOD_1s_3s)))
    val visit_length_4s_6s: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.TIME_PERIOD_4s_6s)))
    val visit_length_7s_9s: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.TIME_PERIOD_7s_9s)))
    val visit_length_10s_30s: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.TIME_PERIOD_10s_30s)))
    val visit_length_30s_60s: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.TIME_PERIOD_30s_60s)))
    val visit_length_1m_3m: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.TIME_PERIOD_1m_3m)))
    val visit_length_3m_10m: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.TIME_PERIOD_3m_10m)))
    val visit_length_10m_30m: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.TIME_PERIOD_10m_30m)))
    val visit_length_30m: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.TIME_PERIOD_30m)))

    val step_length_1_3: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.STEP_PERIOD_1_3)))
    val step_length_4_6: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.STEP_PERIOD_4_6)))
    val step_length_7_9: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.STEP_PERIOD_7_9)))
    val step_length_10_30: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.STEP_PERIOD_10_30)))
    val step_length_30_60: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.STEP_PERIOD_30_60)))
    val step_length_60: Double = show(toLong(StringUtils.getFieldFromConcatString(
      value, "\\|", Constant.STEP_PERIOD_60)))

    // 计算各个访问时长和访问步长的范围
    val visit_length_1s_3s_ratio: Double = NumberUtils.formatDouble(
      visit_length_1s_3s / session_count, 2)
    val visit_length_4s_6s_ratio: Double = NumberUtils.formatDouble(
      visit_length_4s_6s / session_count, 2)
    val visit_length_7s_9s_ratio: Double = NumberUtils.formatDouble(
      visit_length_7s_9s / session_count, 2)
    val visit_length_10s_30s_ratio: Double = NumberUtils.formatDouble(
      visit_length_10s_30s / session_count, 2)
    val visit_length_30s_60s_ratio: Double = NumberUtils.formatDouble(
      visit_length_30s_60s / session_count, 2)
    val visit_length_1m_3m_ratio: Double = NumberUtils.formatDouble(
      visit_length_1m_3m / session_count, 2)
    val visit_length_3m_10m_ratio: Double = NumberUtils.formatDouble(
      visit_length_3m_10m / session_count, 2)
    val visit_length_10m_30m_ratio: Double = NumberUtils.formatDouble(
      visit_length_10m_30m / session_count, 2)
    val visit_length_30m_ratio: Double = NumberUtils.formatDouble(
      visit_length_30m / session_count, 2)

    val step_length_1_3_ratio: Double = NumberUtils.formatDouble(
      step_length_1_3 / session_count, 2)
    val step_length_4_6_ratio: Double = NumberUtils.formatDouble(
      step_length_4_6 / session_count, 2)
    val step_length_7_9_ratio: Double = NumberUtils.formatDouble(
      step_length_7_9 / session_count, 2)
    val step_length_10_30_ratio: Double = NumberUtils.formatDouble(
      step_length_10_30 / session_count, 2)
    val step_length_30_60_ratio: Double = NumberUtils.formatDouble(
      step_length_30_60 / session_count, 2)
    val step_length_60_ratio: Double = NumberUtils.formatDouble(
      step_length_60 / session_count, 2)

    // 将统计结果封装为Domain对象
    val sessionAggrStat = new SessionAggrStat()
    sessionAggrStat.taskid = show(toLong(taskid))
    sessionAggrStat.session_count = session_count
    sessionAggrStat.visit_length_1s_3s_ratio = visit_length_1s_3s_ratio
    sessionAggrStat.visit_length_4s_6s_ratio = visit_length_4s_6s_ratio
    sessionAggrStat.visit_length_7s_9s_ratio = visit_length_7s_9s_ratio
    sessionAggrStat.visit_length_10s_30s_ratio = visit_length_10s_30s_ratio
    sessionAggrStat.visit_length_30s_60s_ratio = visit_length_30s_60s_ratio
    sessionAggrStat.visit_length_1m_3m_ratio = visit_length_1m_3m_ratio
    sessionAggrStat.visit_length_3m_10m_ratio = visit_length_3m_10m_ratio
    sessionAggrStat.visit_length_10m_30m_ratio = visit_length_10m_30m_ratio
    sessionAggrStat.visit_length_30m_ratio = visit_length_30m_ratio
    sessionAggrStat.step_length_1_3_ratio = step_length_1_3_ratio
    sessionAggrStat.step_length_4_6_ratio = step_length_4_6_ratio
    sessionAggrStat.step_length_7_9_ratio = step_length_7_9_ratio
    sessionAggrStat.step_length_10_30_ratio = step_length_10_30_ratio
    sessionAggrStat.step_length_30_60_ratio = step_length_30_60_ratio
    sessionAggrStat.step_length_60_ratio = step_length_60_ratio

    // 调用相应的DAO插入统计结果
    val sessionAggrStatDAO = DAOFactory.getSessionAggrStatDAO()
    sessionAggrStatDAO.insert(sessionAggrStat)
  }

  /**
    * 随机抽取 session
    */
  /*def randomExtractSession(sessionid2AggrInfoRDD:RDD[(String, String)]): Unit ={
    import scala.collection.mutable.Map
    import scala.collection.mutable.ListBuffer
    // 第一步,计算每天每小时的 session 数量, 获取 <yyyy-MM-dd_HH, sessionid> 格式的RDD
    val time2SessionidRDD = sessionid2AggrInfoRDD.map(tuple => {
      val aggrInfo = tuple._2
      val startTime = StringUtils.getFieldFromConcatString(aggrInfo, "\\|", Constant.FIELD_START_TIME)
      val dateHour = DateUtils.getDateHour(startTime)
      (dateHour, aggrInfo)

    })

    // 得到每天每小时的 session 数量
    val countMap = time2SessionidRDD.countByKey()

    /**
      * 第二步,使用按时间比例随机抽取算法,计算出每天每小时要抽取的 session 的索引
      * 将<yyyy-MM-dd_HH,count>格式的map，转换成<yyyy-MM-dd,<HH,count>>的格式
      */
    var dateHourCountMap: Map[String, Map[String, Long]] = Map()
    for (countEntry <- countMap){
      val dateHour = countEntry._1
      val date = dateHour.split("_")(0)
      val hour = dateHour.split("_")(1)
      val count = countEntry._2

      var hourCountMap = dateHourCountMap.getOrElse(date, null)
      if (hourCountMap == null){
        hourCountMap = Map()
        dateHourCountMap += (date -> hourCountMap)
      }

      hourCountMap += (hour -> count)
    }

    // 开始实现按时间比例随机抽取算法
    // 总共要抽取 100 个session, 先按照天数,进行平分
    val extractNumberPerDay = 100 / dateHourCountMap.size

    var dateHourExtractMap: Map[String, Map[String, ListBuffer[Int]]] = Map()

    val random = new Random()

    for(dateHourCountEntry <- dateHourCountMap){
      val date = dateHourCountEntry._1
      var hourCountMap = dateHourCountEntry._2

      // 计算出这一天的session 总数
      var sessionCount = 0L
      for (hourCount <- hourCountMap.values) {
        sessionCount += hourCount
      }

      var hourExtractMap = dateHourExtractMap.getOrElse(date, null)
      if(hourExtractMap == null){
        hourExtractMap = Map()
        dateHourExtractMap += (date -> hourExtractMap)
      }

      // 遍历每个小时
      for (hourCountEntry <- hourCountMap){
        val hour = hourCountEntry._1
        val count = hourCountEntry._2
        // 计算每个小时的 session 数量,占据当天总 session 数量的比例,直接乘以每天要抽取的数量
        var hourExtractNumber = (count.toDouble / sessionCount.toDouble * extractNumberPerDay)
        if(hourExtractNumber > count){
          // 不能超过当天当前小时的总数
          hourExtractNumber = count
        }

        // 现获取当前小时的存放随机数的listBuffer
        var extractIndexList = hourExtractMap.getOrElse(hour, null)
        if(extractIndexList == null){
          extractIndexList = ListBuffer()
          hourExtractMap += (hour -> extractIndexList)
        }

        // 生成上面计算出来的数量的随机数
        for(i <- 0 until hourExtractNumber){
          var extractIndex = random.nextInt(count.toInt)
          while(extractIndexList.contains(count.toInt)){
            extractIndex = random.nextInt(count.toInt)
          }
          extractIndexList += extractIndex
        }
      }
    }
  }*/

  /*def getTop10Category(filterSesssionid2AggrinfoRDD:RDD[(String, String)], sessionid2actionRDD: RDD[(String, Row)])={

    /**
      * 第一步,获取符合条件的 session 访问过的所有品类
      */
    // 获取符合条件的 session 的访问明细
    val session2detailRDD = filterSesssionid2AggrinfoRDD
      .join(session2detailRDD)
      .map(tuple => (tuple._1, tuple._2._2))

    // 获取session 访问过的所有品类id
    // 访问过是指,点击过,下单过,支付过的品类
    val category = session2detailRDD.flatMap(tuple => {
      val row: Row = tuple._2
      val list: List[(Long, Long)] = Array(Tuple2(Long, Long))


    })
  }*/

}
