package sessionApp.jdbc

import java.sql.{Connection, DriverManager, PreparedStatement, ResultSet}

import sessionApp.conf.ConfigurationManager
import sessionApp.constant.Constant

/**
  * 不允许代码中出现硬编码(hard code),所有这些变量需要通过常量封装和使用
  */
class JDBCHelper{

  // 获取数据库连接池的大小,数据库连接池中要放多少个数据库连接
  val datasourceSize: Int = ConfigurationManager.getProperty(Constant.JDBC_DATASOURCE_SIZE).toInt
  val url: String = ConfigurationManager.getProperty(Constant.JDBC_URL)
  val user: String = ConfigurationManager.getProperty(Constant.JDBC_USER)
  val password: String = ConfigurationManager.getProperty(Constant.JDBC_PASSWORD)
  /**
    * 第三步: 实现单例过程中,创建唯一的数据库连接池
    *
    */
  // 创建指定数量的数据库连接,并放入数据库连接池中
  for (i <- 1 to datasourceSize) {
    try {
      val conn: Connection = DriverManager.getConnection(url, user, password)
      // 伴生类可以访问伴生对象的私有属性
      JDBCHelper.datasource += conn
    } catch {
      case ex: Exception => println(ex)
    }
  }


  /**
    * 第四步:
    *   获取数据库连接的方法
    *   有可能去获取的时候,连接都被用光了, 暂时获取不到数据库连接
    *   所以实现一个等待机制,去等待获取到的数据库连接
    * @return
    */
  def getConnection():Connection ={
    while (JDBCHelper.datasource.isEmpty) {
      try {
        Thread.sleep(10)
      }catch{
        case ex: Exception => println(ex)
      }
    }
    val conn = JDBCHelper.datasource(0)
    JDBCHelper.datasource -= conn
    conn
  }

  /**
    * 执行 增删改 操作
    */
  def executeUpdate(sql:String, parmars:Array[Any]):Int = {
    var rtn = 0
    var conn: Connection = null
    var pstmt: PreparedStatement = null
    try {
      conn = getConnection()
      pstmt = conn.prepareStatement(sql)
      println(parmars.length)
      for(i <- 0 until parmars.length ) {
        pstmt.setObject(i + 1, parmars(i))
      }

      rtn = pstmt.executeUpdate()
    } catch {
      case ex: Exception => println(ex)
    } finally {
      if(conn != null){
        JDBCHelper.datasource += conn
      }
    }

    rtn
  }

  /**
    * 执行查询 sql 语句
    */
  def executeQuery(sql:String, params:Array[Any]):ResultSet = {
    var conn: Connection = null
    var pstmt: PreparedStatement = null
    var rs: ResultSet = null

    try {
      conn = getConnection()
      pstmt = conn.prepareStatement(sql)

      for(i <- 0 until params.length) {
        pstmt.setObject(i + 1, params(i))
      }
      rs = pstmt.executeQuery();
    } catch {
      case ex:Exception => println(ex)
    } finally {
      if(conn != null) {
        JDBCHelper.datasource += conn
      }
    }
    rs
  }

  /**
    * 批量执行sql语句
    * @param sql
    * @param paramsList
    */
  def executeBatch(sql:String, paramsList: Array[Array[Any]]): Array[Int]={
    var rtn:Array[Int] = null
    var conn:Connection = null
    var pstmt: PreparedStatement = null

    try {
      conn = getConnection()

      //第一步: 使用 Connection 对象,取消自动提交
      conn.setAutoCommit(false)
      pstmt = conn.prepareStatement(sql)

      // 第二步: 使用 PreparedStatement.addBatch() 方法加入批量的 sql 参数
      for (m <- 0 until paramsList.length) {
        for (n <- 0 until paramsList(m).length){
          pstmt.setObject(n + 1, paramsList(m)(n))
        }
        pstmt.addBatch()
      }

      // 第三步: 使用 PreparedStatement.executeBatch() 方法,批量执行sql
      rtn = pstmt.executeBatch()

      // 第四步: 使用 Connection.commit(), 提交批量的sql语句
      conn.commit()
    } catch {
      case ex:Exception => println(ex)
    }

    rtn
  }
}

object JDBCHelper{
  /**
    * 在静态代码块中,加载数据库驱动
    */
  {
    try {
      val driver = ConfigurationManager.getProperty(Constant.JDBC_DRIVER)
      Class.forName(driver)
    } catch {
      case ex:Exception => println(ex)
    }
  }

  /**
    * 第二步:实现 JDBCHelper 的单例化
    *   为了保证内部封装的数据库连接池有且只有一份
    */
  // 数据库连接池
  private val datasource = scala.collection.mutable.ArrayBuffer[Connection]()

  var instance:JDBCHelper = null
  def getInstance(): JDBCHelper ={
    if (instance == null){
      this.synchronized {
        if (instance == null) {
          instance = new JDBCHelper()
        }
      }
    }
    instance
  }


}