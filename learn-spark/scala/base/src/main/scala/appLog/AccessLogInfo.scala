package appLog

/**
  * 访问日志信息类(可序列化)
  */
@SerialVersionUID(1000L)
class AccessLogInfo(timestamp:Long, upTraffic:Int, downTraffic:Int ) extends Serializable {
  var timestamps: Long = timestamp
  var upTraffics: Int = upTraffic
  var downTraffics: Int = downTraffic
}
