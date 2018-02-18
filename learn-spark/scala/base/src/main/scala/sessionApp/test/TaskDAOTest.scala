package sessionApp.test

import sessionApp.factory.DAOFactory

object TaskDAOTest {

  def main(args: Array[String]): Unit = {
    val taskDAO = DAOFactory.getTaskDAO()
    val task = taskDAO.findById(1)
    while(task.next()){
      val id = task.getInt(1)
      val name = task.getString(2)
      println("id=" + id + ", name=" + name )
    }
  }
}
