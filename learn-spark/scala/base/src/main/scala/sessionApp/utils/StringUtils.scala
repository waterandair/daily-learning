package sessionApp.utils
import scala.util.Try
import util.control.Breaks._

/**
  * 字符串工具类
  */
class StringUtils
object StringUtils {

  /**
    * 判断字符串是否为空
    */
  def isEmpty(str:String): Boolean ={
    str == null || "".equals(str)
  }

  /**
    * 判断字符串是否不为空
    */
  def isNotEmpty(str:String): Boolean ={
    str != null && !"".equals(str)
  }

  /**
    * 补全两位数字
    * @param str
    * @return
    */
  def fulfuill(str: String): String ={
    if(str.length() == 2){
      str
    } else {
      "0" + str
    }
  }

  /**
    * 获取参数值
    * @param string
    * @param delimiter
    * @param field
    * @return
    */
  def getFieldFromConcatString(string: String, delimiter: String, field: String): String ={
    var fieldValue = ""
    try{
      val fields = string.split(delimiter)
      breakable{
        for (elem <- fields){
          val row = elem.split("=")
          if(row.length == 2){
            val fieldName = row(0)
            if(fieldName == field){
              fieldValue = row(1)
              break
            }
          }
        }
      }

      fieldValue
    }catch{
      case ex:Exception =>
        println(ex)
        fieldValue
    }
  }

  /**
    * 从拼接的字符串中给字段设置值
    * @param str  字符串
    * @param delimiter  分隔符
    * @param field  字段名
    * @param newFieldValue  新的 field 值
    */
  def setFieldFromConcatString(str: String, delimiter: String, field: String, newFieldValue: String): String ={
    val fields = str.split(delimiter)

    breakable{
      for (i <- 0 until fields.length) {

        val fieldsKey = fields(i).split("=")(0)
        if (fieldsKey == field){
          val concatField = field + "=" + newFieldValue
          fields(i) = concatField
          break
        }
      }
    }
    fields.mkString("|")

  }

  def tryToInt( s: String ) = {
    val res = Try(s.toInt).toOption
    res match {
      case Some(s) => s
      case None => "?"
    }
  }

}
