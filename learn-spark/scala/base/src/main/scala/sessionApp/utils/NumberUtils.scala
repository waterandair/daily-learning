package sessionApp.utils

class NumberUtils
object NumberUtils{

  /**
    * 格式化小数
    * @param num 浮点数
    * @param scale 位数
    */
  def formatDouble (num: Double, scale: Int): Double ={
    val bd = BigDecimal(num)
    bd.setScale(scale, BigDecimal.RoundingMode.HALF_UP).doubleValue()
  }
}
