package sessionApp.utils

import java.text.SimpleDateFormat
import java.util.Date

import org.joda.time.DateTime

class DateUtils
object DateUtils {
  val DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd")
  val TIME_FORMAT = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
  val DATEKEY_FORMAT = new SimpleDateFormat("yyyyMMdd")


  /**
    * 获取今天的日期
    * @return
    */
  def getTodayDate(): String ={
    DATE_FORMAT.format(new Date())
  }

  /**
    * 解析字符串时间
    * @param str
    * @return
    */
  def parseTime(str: String):Date = {
    var date: Date = null
    try {
      date = TIME_FORMAT.parse(str)
    }catch {
      case ex: Exception => println(ex)
    }
    date
  }

  /**
    * 获取年月日和小时
    * @param dateTime yyyy-MM-dd HH:mm:ss
    * @return yyyy-MM-dd_HH
    */
  def getDateHour(dateTime: String): String ={
    val date = dateTime.split(" ")(0)
    val hourMinuteSecond = dateTime.split(" ")(1)
    val hour = hourMinuteSecond.split(":")(0)
    date + "_" + hour
  }
}
