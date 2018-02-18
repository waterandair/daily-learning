package sessionApp.conf

import java.util.Properties

/**
  * 配置管理组件
  */
class ConfigurationManager

object ConfigurationManager{
  private val prop = new Properties()

  // 伴生对象中的代码块,相当于 java 中的静态代码块
  {
    try {
      // 通过一个“类名.class”的方式，就可以获取到这个类在JVM中对应的Class对象
      // 然后再通过这个Class对象的getClassLoader()方法，就可以获取到当初加载这个类的JVM
      // 中的类加载器（ClassLoader），然后调用ClassLoader的getResourceAsStream()这个方法
      // 就可以用类加载器，去加载类加载路径中的指定的文件
      // 最终可以获取到一个，针对指定文件的输入流（InputStream）
      val in = ConfigurationManager.getClass.getClassLoader.getResourceAsStream("my.properties")
      prop.load(in)
    } catch {
      case ex: Exception => println(ex)
    }

  }

  def getProperty(key:String): String = {
    /* 第一次外界代码,调用 ConfigurationManager 类的 getProperty 静态方法时,JVM N内部会发现 ConfigurationManager 类还不在内存中
       此时, JVM 就会 使用自己的 ClassLoader (类加载器), 去对应的类所在的磁盘文件(.class文件) 中去加载 ConfigurationManager 类, 到
       JVM 内存中来,并根据类内部的信息,去创建一个 class 对象
       class 对象中,就包含了类的元信息
       加载ConfigurationManager类的时候，还会初始化这个类，此时静态代码块中的代码，就会加载my.properites文件的内容，到Properties对象中来
       下一次外界代码，再调用ConfigurationManager的getProperty()方法时，就不会再次加载类，不会再次初始化
       类，和执行静态代码块了，所以，类只会加载一次，配置文件也仅仅会加载一次
    */
    prop.getProperty(key)
  }

}
