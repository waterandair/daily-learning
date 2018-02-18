package sessionApp.test

import java.sql.{Connection, DriverManager, PreparedStatement, ResultSet, Statement}

class JdbcCRUD
object JdbcCRUD {
  def main(args: Array[String]): Unit = {
    insert()
    //preparedStateMent()
    select()

  }

  /**
    * 测试插入数据
    * jdbc 的基本使用:
    *   1、加载驱动类：Class.forName()
    *   2、获取数据库连接：DriverManager.getConnection()
    *   3、创建SQL语句执行句柄：Connection.createStatement()
    *   4、执行SQL语句：Statement.executeUpdate()
    *   5、释放数据库连接资源：finally，Connection.close()
    */
  def insert(): Unit = {
    var conn:Connection = null
    var stmt:Statement = null

    try {
      /**
        * 第一步:
        *   Class.forName() 是java提供的一种基于反射的方式,直接根据类的全限定名(包+类)从类所在的磁盘文件
        *   (.class)文件中加载类对应的内容,并创建对应的class对象
        */
      val driver = "com.mysql.jdbc.Driver"
      Class.forName(driver)

      /**
        * 第二步:获取数据库连接
        *   使用 DriverManager.getConnection() 方法获取针对数据库的连接
        *   需要给方法传入三个参数,包括 url,user,password
        *   其中,url就是有特定格式的数据库连接串,包括 "主协议://主机名:端口号/数据库"
        */
      conn = DriverManager.getConnection(
        "jdbc:mysql://localhost:3306/spark_project?characterEncoding=utf8",
        "root",
        "000000"
      )

      /**
        * 第三步: 基于数据库连接 Connection 对象,创建 sql 语句执行句柄, Statement 对象
        *   Statement 对象,就是用来基于底层的 Connection 代表的数据库连接
        *   允许我们通过java程序,通过 Statement 对象,向 mysql 数据库发送 sql 语句
        *   从而实现通过发送的 sql 语句来执行增删改查
        */
      stmt = conn.createStatement()

      /**
        * 第四步: 执行 sql 语句
        *   executeUpdate() 方法,可以执行 insert, update, delete 语句
        *   返回类型是 int 值,是 sql 语句影响的行数
        */
      val sql = "insert into test_user(name,age) values('李四',26)"
      val rtn = stmt.executeUpdate(sql)
      println("sql 语句影响了[" + rtn + "]")
    } catch {
      case ex:Exception => println(ex)
    }finally {
      /**
        * 最后要在 finally 代码块中, 尽快再执行完 sql 语句之后,就释放数据库;连接
        */
      try {
        if(stmt != null) {
          stmt.close()
        }
        if(conn != null) {
          conn.close()
        }
      } catch {
        case ex:Exception => println(ex)
      }
    }

  }

  /**
    * 测试查询数据
    */
  def select(): Unit ={
    var conn:Connection = null
    var stmt:Statement = null
    var rs: ResultSet = null

    try {
      val driver = "com.mysql.jdbc.Driver"
      Class.forName(driver)

      conn = DriverManager.getConnection(
        "jdbc:mysql://localhost:3306/spark_project",
        "root",
        "000000"
      )

      stmt = conn.createStatement()

      val sql = "select * from test_user"

      val rs = stmt.executeQuery(sql)

      while(rs.next()){
        val id = rs.getInt(1)
        val name = rs.getString(2)
        val age = rs.getInt(3)
        println("id=" + id + ", name=" + name + ", age=" + age)
      }
    } catch {
      case ex:Exception => println(ex)
    }finally {
      /**
        * 最后要在 finally 代码块中, 尽快再执行完 sql 语句之后,就释放数据库;连接
        */
      try {
        if(stmt != null) {
          stmt.close()
        }
        if(conn != null) {
          conn.close()
        }
      } catch {
        case ex:Exception => println(ex)
      }
    }

  }



  /**
    * 使用 statement ,第一容易引发sql注入,第二性能底下
    * 使用 preparedStatement 第一,用 ? 占位符,防止sql注入,第二,相同结构的sql 语句只会编译一次,下一次只需要改变参数就可以了
    */
  def preparedStateMent(): Unit = {
    var pstmt:PreparedStatement = null
    var conn:Connection = null
    try {
      val driver = "com.mysql.jdbc.Driver"
      Class.forName(driver)
      conn = DriverManager.getConnection(
        "jdbc:mysql://localhost:3306/spark_project?characterEncoding=utf8",
        "root",
        "000000"
      )

      val sql = "insert into test_user(name,age) values(?,?)"
      pstmt = conn.prepareStatement(sql)

      pstmt.setString(1, "李四")
      pstmt.setInt(2, 26)

      val rtn = pstmt.executeUpdate()
      println("sql 语句影响了["+ rtn +"] 行.")

    } catch {
      case ex: Exception => println(ex)
    } finally {
      try {
        if(pstmt != null) {
          pstmt.close()
        }
        if(conn != null) {
          conn.close()
        }
      } catch {
        case ex: Exception => println(ex)
      }
    }
  }
}
