package sessionApp.factory

import sessionApp.dao.ITaskDAO
import sessionApp.dao.impl.{SessionAggrStatDAOImpl, TaskDAOImpl}

class DAOFactory
object DAOFactory{
  def getTaskDAO():TaskDAOImpl={
    val taskdao = new TaskDAOImpl()
    taskdao
  }

  def getSessionAggrStatDAO(): SessionAggrStatDAOImpl= {
    val dao = new SessionAggrStatDAOImpl()
    dao
  }
}
