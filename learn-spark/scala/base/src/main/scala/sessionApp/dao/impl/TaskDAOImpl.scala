package sessionApp.dao.impl

import java.sql.ResultSet

import sessionApp.domain.Task
import sessionApp.dao.ITaskDAO
import sessionApp.jdbc.JDBCHelper

class TaskDAOImpl extends ITaskDAO {

  /**
    * 根据主键查询任务
    */
  def findById(taskid: Long): ResultSet = {
    val task = new Task()
    val sql = "select * from task where task_id=?"
    val jdbcHelper = JDBCHelper.getInstance()
    val params: Array[Any] = Array(taskid)

    val res = jdbcHelper.executeQuery(sql, params)
    if (res.next()){
      res
    } else {
      null
    }
  }
}
