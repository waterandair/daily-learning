package sessionApp.dao

import java.sql.ResultSet

/**
  * 任务管理 DAO 接口
  */
trait ITaskDAO {
  def findById(taskid: Long): ResultSet
}
