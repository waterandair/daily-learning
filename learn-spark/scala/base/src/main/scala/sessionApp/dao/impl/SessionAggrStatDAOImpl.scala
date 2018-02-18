package sessionApp.dao.impl

import sessionApp.dao.ISessionAggrStat
import sessionApp.domain.SessionAggrStat
import sessionApp.jdbc.JDBCHelper

class SessionAggrStatDAOImpl extends ISessionAggrStat{
  /**
    * 插入 session 聚合统计结果
    * @param sessionAggrStat
    */
  override def insert(sessionAggrStat: SessionAggrStat): Unit = {
    val sql = "insert into session_aggr_stat values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    val params: Array[Any] = Array(
      sessionAggrStat.taskid,
      sessionAggrStat.session_count,
      sessionAggrStat.visit_length_1s_3s_ratio,
      sessionAggrStat.visit_length_4s_6s_ratio,
      sessionAggrStat.visit_length_7s_9s_ratio,
      sessionAggrStat.visit_length_10s_30s_ratio,
      sessionAggrStat.visit_length_30s_60s_ratio,
      sessionAggrStat.visit_length_1m_3m_ratio,
      sessionAggrStat.visit_length_3m_10m_ratio,
      sessionAggrStat.visit_length_10m_30m_ratio,
      sessionAggrStat.visit_length_30m_ratio,
      sessionAggrStat.step_length_1_3_ratio,
      sessionAggrStat.step_length_4_6_ratio,
      sessionAggrStat.step_length_7_9_ratio,
      sessionAggrStat.step_length_10_30_ratio,
      sessionAggrStat.step_length_30_60_ratio,
      sessionAggrStat.step_length_60_ratio
    )
    val jdbcHelper = JDBCHelper.getInstance()
    jdbcHelper.executeUpdate(sql, params)
  }

}
