package sessionApp.utils

import com.alibaba.fastjson.{JSON, JSONObject}
import sessionApp.conf.ConfigurationManager
import sessionApp.constant.Constant

class ParamUtils
object ParamUtils{
  // 命令行参数中提取任务id
  def getTaskIdFromArgs(args:Array[String], taskType: String): Long = {
    val local = ConfigurationManager.getProperty(Constant.SPARK_LOCAL).toBoolean
    if (local) {
      ConfigurationManager.getProperty(taskType).toLong
    } else {
      try{
        if (args != null && args.length > 0) {
          args(0).toLong
        }else{
          0L
        }
      } catch {
        case ex:Exception =>
          println(ex)
          0L
      }
    }
  }

  /**
    * 从json对象中提取参数
    */
  def getParam(jsonObject: JSONObject, field: String): String ={
    val jsonArray = jsonObject.get(field)
    jsonArray.toString
  }
}
