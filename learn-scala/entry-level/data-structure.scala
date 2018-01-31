/**
  * Array 定长数组
  */
val intValueArr = new Array[Int](3)   // 声明一个长度为3的整型数组,每个数组元素初始化为0
intValueArr(0) = 12 // 给第1个元素赋值
intValueArr(1) = 45 // 给第2个元素赋值
intValueArr(2) = 33

val myStrArr = new Array[String](3)   // 声明一个长度为3的字符串数组,每个数组元素初始化为null
myStrArr(0) = "BigData"
myStrArr(1) = "Hadoop"
myStrArr(2) = "Spark"
for (i <- 0 to 2) println(myStrArr(i))

// 简洁数据声明和初始化方法
val intValueArr2 = Array(1, 2, 3)
val myStrArr2 = Array("a", "b", "3")
for (i <- 0 to 2) println(intValueArr2(i))
println("-"*30)

/**
  *  List 列表
  */
val intList = List(1, 2, 3)
println(intList.head)  // 头部 Int 1
println(intList.tail)  // 尾部 List(2, 3)

// 在列表的头部增加新的元素
val intListOther = 0 :: intList
println(intListOther)  //List(0, 1, 2, 3)
// :: 操作符是右结合的,因此,如果要构建一个列表 List(1, 2, 3), 实际上也可以采用下面的方式
val intListOther2 = 1 :: 2 :: 3 :: Nil
// 也可以使用 ::: 操作符对不同的列表进行连接得到新的列表
val intList1 = List(1, 2)
val intList2 = List(3, 4)
val intList3 = intList1 ::: intList2
println(intList3)

// scala 为列表提供了一些常用的方法
val sum = intList.sum  //求和
println(sum)

println("-"*30)

/**
  * tuple 元组
  */
val tuple = ("BigData", 2018, 45.0)
println(tuple._1)
println(tuple._2)
println(tuple._3)
println("-"*30)

/**
  * Set 集
  * 集包括可变集和不可变集,默认情况下是不可变集,如果要声明一个可变集,需要引入 scala.collection.mutable.Set包
  * 区别:
  *     对不可变集进行操作,会产生一个新的集,原来的集并不发生变化.而对可变集进行的操作,改变的是该集本身
  */
var mySet = Set("Hadoop", "Spark")
mySet += "Scala"  // 向 mySet 中增加新的元素
println(mySet.contains("Scala"))

import scala.collection.mutable.Set
val myMutableSet = Set("Database", "BigData")
myMutableSet += "Cloud Computing"
println(myMutableSet)    //Set(BigData, Cloud Computing, Database)
println("-"*30)

/**
  * Map 映射
  * 映射包括可变和不可变.默认是不可变映射,创建可变映射,需要引入 scala.collection.mutable.Map
  */
val university = Map("XMU" -> "Xiamen University", "THU" -> "Tsinghua University", "PKU" -> "Peking University")
println(university("XMU"))  // 根据键获取映射中的值
println(university.contains("XMU"))  // 判断键是否存在

// 可变的映射
import scala.collection.mutable.Map
val university2 = Map("XMU" -> "Xiamen University", "THU" -> "Tsinghua University", "PKU" -> "Peking University")
university2("XMU") = "XMU"  // 更新元素
university2("FZU") = "Fuzhou University"  // 添加元素
// 也可以使用 += 操作来添加新的元素
university2 += ("SDU" -> "Tianjin University", "WHU" -> "Wuhan University")  // 添加一个新元素
println(university2)

// 循环遍历映射 for((k, v) <- 映射) 语句块
for ((k, v) <- university2) printf("%s -> %s\n", k, v)
// 只遍历 key 或value
for (k <- university2.keys) println(k)
for (v <- university2.values) println(v)
println("-"*30)

/**
  * 迭代器 (iterator)
  * 不是一个集合,但是提供了访问集合的一种方法.当构建一个集合需要很多的开销时,迭代器可以发挥很好的性能
  * 注意:
  *     遍历一遍后,迭代器会移动到末尾,变为empty iterator, 就不能再使用了,
  */
val iter = Iterator("Hadoop", "Spark", "Scala")
while (iter.hasNext) {
  println(iter.next())
}
println(iter)  // empty iterator

val iter2 = Iterator("Hadoop", "Spark", "Scala")
for (elem <- iter2) {
  println(elem)
}



















