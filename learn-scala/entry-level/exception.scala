/**
  * 异常
  * Scala 的方法可以通过抛出异常的方法的方式来终止相关代码的运行，不必通过返回值。
  * eg. 跑出一个新的参数异常 throw new IllegalArgumentException
  */

try {
  throw new IllegalArgumentException("x should not be negative")
} catch {
  case _: IllegalArgumentException => println("Illegal Argument!")
} finally {
  println("release resources!")
}

import java.io.IOException
try {
  throw new IOException("user defined exception")
} catch {
  case e1: IllegalArgumentException => println("illegal argument")
  case e2: IOException => println("io exception")
}