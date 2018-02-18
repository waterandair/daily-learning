package sessionApp.dao

import sessionApp.domain.SessionAggrStat
/**
  * session 聚合统计模块 DAO 接口
  */
trait ISessionAggrStat {

  def insert(sessionAggrStat: SessionAggrStat)

}
