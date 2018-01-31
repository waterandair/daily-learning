val x = 6
if (x>0) {
  println("this is a positive number")
} else {
  println("this is not a positive number")
}

// 特别的一点, if 表达式的值可以赋值给变量
val a = if (x>0) 1 else -1
println(a)

// if 和 else 子句中的值类型可能不同,scala 会自动进行推断,取两个类型的公共类型,通常是Any

// 跳出循环语句
// scala 没有提供break语句
// 但是可以使用 boolean 类型变量, return 或者 Breaks 的 break 函数来替代使用
import scala.util.control.Breaks.break
