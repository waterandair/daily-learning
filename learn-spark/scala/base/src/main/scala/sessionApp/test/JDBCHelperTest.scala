package sessionApp.test
import sessionApp.jdbc.JDBCHelper
object JDBCHelperTest {
  def main(args: Array[String]): Unit = {
    // 获取 jdbchelper 的单例
    val jdbcHelper: JDBCHelper = JDBCHelper.getInstance()
    // 测试普通的增删改查语句
    val rtn = jdbcHelper.executeUpdate("insert into test_user(name,age) values(?, ?)", Array("张吉", 24))
    println(rtn)

    // 测试 select
    val res = jdbcHelper.executeQuery("select * from test_user where name = ?", Array("张吉"))
    while(res.next()){
      val id = res.getInt(1)
      val name = res.getString(2)
      val age = res.getInt(3)
      println("id=" + id + ", name=" + name + ", age=" + age)
    }

    // 测试批量执行 sql 语句
    val sql = "insert into test_user(name, age) values(?, ?)"
    val paramsList = Array(
      Array("李飞", 18),
      Array("李飞飞", 19)
    )
    val rtn2 = jdbcHelper.executeBatch(sql, paramsList)
    println(rtn2.toList)
  }


}
