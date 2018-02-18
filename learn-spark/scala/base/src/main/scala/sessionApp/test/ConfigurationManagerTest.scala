package sessionApp.test

import sessionApp.conf.ConfigurationManager

object ConfigurationManagerTest {
  def main(args: Array[String]): Unit = {
    val testKey1 = ConfigurationManager.getProperty("testkey1")
    val testKey2 = ConfigurationManager.getProperty("testkey2")

    println(testKey1)
    println(testKey2)
  }
}
