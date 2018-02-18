package sessionApp.test

import com.alibaba.fastjson.JSON

/**
  * fastjson 测试类
  */
object FastJsonTest {
  def main(args: Array[String]): Unit = {
    val json = "[{'学生':'张三', '班级':'一班', '年级':'大一', '科目':'高数', '成绩':90}, {'学生':'李四', '班级':'二班', '年级':'大一', '科目':'高数', '成绩':80}]"

    val jsonArray = JSON.parseArray(json)
    val jsonObject = jsonArray.getJSONObject(0)
    println(jsonObject.get("学生"))
  }
}
