// 写文件
import java.io.PrintWriter  // scala需要使用 java.io.PrintWriter 实现把数据写入到文本文件
val out = new PrintWriter("output.txt")  // 如果没有给出文件路径,则默认生成文件到当前目录下
for (i <- 1 to 6) out.println(i)
out.close()


// 读文件
import scala.io.Source
val inputFile = Source.fromFile("output.txt")
val lines = inputFile.getLines()
for (line <- lines) println(line)


/**
  * lazy 特性
  * 如果将一个变量声明为 lazy, 则只有再第一次使用该变量时,变量对应的表达式才会发生计算
  * 这种特性对于特别耗时的计算操作特别有用,比如打开文件进行 IO, 进行网络 IO 等
  */
// 即使文件不存在，也不会报错，只有第一个使用变量时会报错
lazy val file = Source.fromFile("output.txt").mkString
println(file)
