package sessionApp.constant

/**
  * 常量接口
  */
object Constant {
  // 项目配置相关的常量
  val JDBC_DRIVER : String = "jdbc.driver"
  val JDBC_DATASOURCE_SIZE : String = "jdbc.datasource.size"
  val JDBC_URL : String = "jdbc.url"
  val JDBC_USER : String= "jdbc.user"
  val JDBC_PASSWORD : String= "jdbc.password"
  val SPARK_LOCAL = "spark.local"
  val SPARK_LOCAL_TASKID_SESSION = "spark.local.taskid.session"
  val SPARK_LOCAL_TASKID_PAGE = "spark.local.taskid.page"
  val SPARK_LOCAL_TASKID_PRODUCT = "spark.local.taskid.product"

  // spark 作业相关的常量
  val SPARK_APP_NAME_SESSION: String = "UserVisitSessionAnalyzeSpark"
  val SPARK_APP_NAME_PAGE: String = "PageOneStepConvertRateSpark"
  val FIELD_SESSION_ID: String = "sessionid"
  val FIELD_SEARCH_KEYWORDS: String = "searchKeywords"
  val FIELD_CLICK_CATEGORY_IDS: String = "clickCategoryIds"
  val FIELD_AGE: String = "age"
  val FIELD_PROFESSIONAL: String = "professional"
  val FIELD_CITY: String = "city"
  val FIELD_SEX: String = "sex"
  val FIELD_VISIT_LENGTH: String = "visitLength"
  val FIELD_STEP_LENGTH: String = "stepLength"
  val FIELD_START_TIME: String = "startTime"
  val FIELD_CLICK_COUNT: String = "clickCount"
  val FIELD_ORDER_COUNT: String = "orderCount"
  val FIELD_PAY_COUNT: String = "payCount"
  val FIELD_CATEGORY_ID: String = "categoryid"

  val SESSION_COUNT: String = "session_count"

  val TIME_PERIOD_1s_3s: String = "1s_3s"
  val TIME_PERIOD_4s_6s: String = "4s_6s"
  val TIME_PERIOD_7s_9s: String = "7s_9s"
  val TIME_PERIOD_10s_30s: String = "10s_30s"
  val TIME_PERIOD_30s_60s: String = "30s_60s"
  val TIME_PERIOD_1m_3m: String = "1m_3m"
  val TIME_PERIOD_3m_10m: String = "3m_10m"
  val TIME_PERIOD_10m_30m: String = "10m_30m"
  val TIME_PERIOD_30m: String = "30m"

  val STEP_PERIOD_1_3: String = "1_3"
  val STEP_PERIOD_4_6: String = "4_6"
  val STEP_PERIOD_7_9: String = "7_9"
  val STEP_PERIOD_10_30: String = "10_30"
  val STEP_PERIOD_30_60: String = "30_60"
  val STEP_PERIOD_60: String = "60"

  // 任务相关常量
  val PARAM_START_DATE: String = "startDate"
  val PARAM_END_DATE: String = "endDate"
  val PARAM_START_AGE: String = "startAge"
  val PARAM_END_AGE: String = "endAge"
  val PARAM_PROFESSIONALS: String = "professionals"
  val PARAM_CITIES: String = "cities"
  val PARAM_SEX: String = "sex"
  val PARAM_KEYWORDS: String = "keywords"
  val PARAM_CATEGORY_IDS: String = "categoryIds"
  val PARAM_TARGET_PAGE_FLOW: String = "targetPageFlow"
}
