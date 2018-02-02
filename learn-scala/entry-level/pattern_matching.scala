/**
  * 不同于其他语言中的 switch case,
  * scala 提供了 match case 语法
  * switch case 只能匹配变量的值,
  * scala match case 可以匹配各种情况, 比如变量的类型,集合的元素,有值或无值
  *
  * 变量 match {case 值 => 代码}
  * 如果值为下划线,代表不满足以上所有情况下的默认情况如何处理
  */

def judgeGrade(grade: String, name: String = ""): Unit = {
  grade match {
    case "A" => println("excellent")
    case "B" => println("good")
    case "C" => println("just so so")
    case _ if name == "zj" => println("zj")
    // 可以把要匹配的值,在这里赋值给一个变量,可以在后面的逻辑中使用
    case _grade2 => println("you need work hard, your grade is " + _grade2)
  }
}

judgeGrade("A")


// 匹配类型 , 语法要用 " case 变量: 类型 => 代码"
import java.io._
def processException(e: Exception): Unit = {
  e match {
    case e1: IllegalArgumentException => println(e1)
    case e2: FileNotFoundException => println("找不到文件" + e2)
    case e3: IOException => println("Io 错误" + e3)
    case _: Exception =>
  }
}

// 对 Array 和 List 进行模式匹配
// 对 Array 和 List 进行模式匹配,分别可以匹配符带有指定元素的数组,指定个数的数组,以某元素打头数组
// 对 List 进行模式匹配, 与 Array 类似, 但是需要使用 List 特有的 :: 操作符
def greeting(arr: Array[String]): Unit = {
  arr match {
    case Array("Leo") => println("Hi, Leo")
    case Array("a", "b", "c") => println(arr)
    case Array("Leo", _*) => println("匹配以元素 Leo 开头的数组 " )
    case _ => println("...")
  }
}

def greeting(list: List[String]): Unit = {
  list match {
    case "Leo" :: Nil => println("匹配到以 Leo 开头的list")
    case "a" :: "b" :: "c" :: Nil => println("")
  }
}

/**
  * case class 样例类
  */

class Person
case class Teacher(name: String, subject: String) extends Person
case class Student(name: String, classroom: String) extends Person

def judgeIdentify(p: Person) {
  p match {
    case Teacher(name, subject) => println("Teacher, name is " + name + ", subject is " + subject)
    case Student(name, classroom) => println("Student, name is " + name + ", classroom is " + classroom)
    case _ => println("Illegal access, please go out of the school!")
  }
}

/**
  * Option
  * 一种特殊的类型,有两种值, 一种是 Some, 表示有值, 一种是 None, 表示没有值
  * Option 通常会用于模式匹配中,用于判断某个变量是否有值,这比 null 更加简洁
  *
  */
val grades = Map("Leo" -> "A", "Jack" -> "B", "Jen" -> "C")

def getGrade(name: String) {
  val grade = grades.get(name)
  grade match {
    case Some(grade) => println("your grade is " + grade)
    case None => println("Sorry, your grade information is not in the system")
  }
}

