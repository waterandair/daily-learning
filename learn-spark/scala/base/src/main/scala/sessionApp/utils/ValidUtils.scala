package sessionApp.utils

/**
  * 校验工具类
  */
class ValidUtils
object ValidUtils{

  /**
    * 校验数据中的指定字段,是否再指定范围内
    * @param data 数据
    * @param dataField 数据字段
    * @param parameter 参数
    * @param startParamField 起始参数字段
    * @param endParamField 结束参数字段
    */
  def between(data: String, dataField: String, parameter: String, startParamField: String, endParamField: String): Boolean ={
    val startParamFieldStr = StringUtils.getFieldFromConcatString(parameter, "\\|", startParamField)
    val endParamFieldStr = StringUtils.getFieldFromConcatString(parameter, "\\|", endParamField)
    if (startParamFieldStr == null || endParamFieldStr == null) {
      true
    } else {
      val startParamFieldValue = startParamFieldStr.toInt
      val endParamFieldVlaue = endParamFieldStr.toInt
      val dataFieldStr = StringUtils.getFieldFromConcatString(data, "\\|", dataField)

      if (dataFieldStr != null) {
        val dataFieldValue = dataFieldStr.toInt
        if (dataFieldValue >= startParamFieldValue && dataFieldValue <= endParamFieldVlaue) {
          true
        } else {
          false
        }
      } else {
        false
      }
    }

  }

  /**
    * 校验数据中的指定字段,是由于有值与参数字段的值相同
    * @param data 数据
    * @param dataField 数据字段
    * @param parameter 参数
    * @param paramField 参数字段
    * @return 校验结果
    */
  def in(data: String, dataField: String, parameter: String, paramField: String): Boolean ={
    val paramFieldValue = StringUtils.getFieldFromConcatString(parameter, "\\|", paramField)
    if (paramFieldValue == null) false
    val paramFieldValueSplited = paramFieldValue.split(",")

    val dataFieldValue = StringUtils.getFieldFromConcatString(data, "\\|", dataField)
    var equals = false
    if (dataFieldValue != null) {
      val dataFieldValueSplited = dataFieldValue.split(",")
      for(singleDataFieldValue <- 0 until dataFieldValueSplited.length){
        for(singleParamFieldValue <- 0 until paramFieldValueSplited.length){
          if (singleDataFieldValue.equals(singleParamFieldValue)) {
            equals = true
          }
        }
      }

    } else {
      equals = false
    }

    equals
  }


  /**
    * 校验数据中的指定字段,是否再指定范围内
    * @param data 数据
    * @param dataField 数据字段
    * @param parameter  参数
    * @param paramField 参数字段
    * @return
    */
  def equal(data: String, dataField: String, parameter: String, paramField: String): Boolean ={
    val paramFieldValue = StringUtils.getFieldFromConcatString(parameter, "\\|", paramField)
    if (paramFieldValue == null) true

    val dataFieldValue = StringUtils.getFieldFromConcatString(data, "\\|", dataField)
    if (dataFieldValue != null) {
      if (dataFieldValue.equals(paramFieldValue)) true else false
    } else {
      false
    }
  }


}