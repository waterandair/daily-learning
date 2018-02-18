package sessionApp.test

class Singleton
object Singleton{
  private var instance:Singleton = null
  private def apply: Singleton = new Singleton()

  def getInstance():  Singleton ={
    // 多个线程过来的时候,判断 instance 是否为 null
   if (instance == null) {
     // 在这里进行多个线程的同步
     // 同一时间,只能有一个线程获取到 Singleton Class 对象的锁
     // 其他线程等待
     this.synchronized {
       if (instance == null) instance = new Singleton()
     }
   }
    instance
  }

}
