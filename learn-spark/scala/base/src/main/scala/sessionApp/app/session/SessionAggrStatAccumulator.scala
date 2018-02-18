package sessionApp.app.session

import org.apache.spark.util.AccumulatorV2
import sessionApp.constant.Constant
import sessionApp.utils.StringUtils
import scala.util.Try

class SessionAggrStatAccumulator extends AccumulatorV2[String, String]{
  /**
    * 自定义Accumulator, 需要实现 AccumulatorV2(2.0版本之前是AccumulatorParam) 接口,并使用 [] 语法,定义输入输出的数据格式
    */

  val zero =  Constant.SESSION_COUNT + "=0|" +
    Constant.TIME_PERIOD_1s_3s + "=0|" +
    Constant.TIME_PERIOD_4s_6s + "=0|" +
    Constant.TIME_PERIOD_7s_9s + "=0|" +
    Constant.TIME_PERIOD_10s_30s + "=0|" +
    Constant.TIME_PERIOD_30s_60s + "=0|" +
    Constant.TIME_PERIOD_1m_3m + "=0|" +
    Constant.TIME_PERIOD_3m_10m + "=0|" +
    Constant.TIME_PERIOD_10m_30m + "=0|" +
    Constant.TIME_PERIOD_30m + "=0|" +
    Constant.STEP_PERIOD_1_3 + "=0|" +
    Constant.STEP_PERIOD_4_6 + "=0|" +
    Constant.STEP_PERIOD_7_9 + "=0|" +
    Constant.STEP_PERIOD_10_30 + "=0|" +
    Constant.STEP_PERIOD_30_60 + "=0|" +
    Constant.STEP_PERIOD_60 + "=0"

  var res:String = zero
  /**
    * 累加操作
    * @param v
    */
  override def add(v: String): Unit = {
    var v1 = res
    var v2 = v

    val oldValue = StringUtils.getFieldFromConcatString(res, "\\|", v2)
    // 累加 1
    val newValue = oldValue.toInt + 1
    // 给连接串中的 v2 设置新的累加后的值
    res = StringUtils.setFieldFromConcatString(res, "\\|", v2, newValue.toString)

  }

  /**
    * 重置
    */
  override def reset(): Unit = {
    res = zero
  }

  override def value: String = {
    res
  }

  override def isZero: Boolean = {
    res == zero
  }

  override def copy(): AccumulatorV2[String, String] = {
    val sessionAggrStatAccumulator = new SessionAggrStatAccumulator()
    sessionAggrStatAccumulator.res = this.res
    sessionAggrStatAccumulator
  }


  override def merge(other: AccumulatorV2[String, String])=other match {
    case o :  SessionAggrStatAccumulator => {
      val res1Map = res.split("\\|").map(line => {
        val lineArr = line.split("=")
        Map(lineArr(0) -> lineArr(1).toInt)
      }).reduce(_ ++ _)

      val res2Map = o.res.split("\\|").map(line => {
        val lineArr = line.split("=")
        Map(lineArr(0) -> lineArr(1).toInt)
      }).reduce(_ ++ _)

      // 相同的key
      val sameFields = res1Map.keys.toSet.&(res2Map.keys.toSet)
      val sameFieldsMap = sameFields.map(field => {
        Map(field -> (res1Map.getOrElse(field, 1) + res2Map.getOrElse(field, 1)))
      }).reduce(_ ++ _)

      val resultsMap = res1Map ++ res2Map ++ sameFieldsMap

      res = resultsMap.map(v => v._1 + "=" + v._2).mkString("|")
    }
    case _ => {throw new UnsupportedOperationException(
      s"Cannot merge ${this.getClass.getName} with ${other.getClass.getName}")
    }
  }



}
