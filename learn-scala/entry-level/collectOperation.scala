/**
  * 遍历操作
  */
// 列表的遍历
val list = List(1, 2, 3)
// for
for (elem <- list) println(elem)
// foreach
list.foreach(elem => println(elem))
// 简写
list.foreach(println)
list foreach println
println("-"*30)


// 映射的遍历
val letters = Map("a" -> "A", "b" -> "B", "c" -> "C")
// for
for ((k, v) <- letters) printf("%s -> %s\n", k, v)  // 也可以仅遍历键或值, letters.keys letters.values
// foreach
letters foreach {case(k, v) => println(k + ":" + v)}
letters foreach {kv => println(kv._1 + "=" + kv._2)}
letters.foreach(kv => println(kv._1 + "-" + kv._2))


/**
  * map 操作和 flatMap 操作
  */
//map
val books = List("hadoop", "hive", "hdfs")
val books2 = books.map(s => s.toUpperCase)
println(books2)  // List(HADOOP, HIVE, HDFS)

//faltMap 传入一个函数,对每一个输入都返回一个集合,而不是一个元素,然后faltMap把生成的多个集合合并为一个集合
val res = books flatMap(s => s.toList)
println(res)  // List(h, a, d, o, o, p, h, i, v, e, h, d, f, s)


/**
  * filter操作
  * 遍历一个集合,并从中获取满足指定条件的元素组成的一个新的集合
  */
val has_a = letters.filter(kv => kv._1.contains("a"))
println(has_a)  // Map(a -> A)


/**
  * reduce 操作
  * reduce 分为两种,reduceLeft 和 reduceRight, 默认是 reduceLeft.
  * 注意 reduceLeft 和 reduceRight 的结果不一定是相同的
  * 对于 List(1, 2, 3).reduceLeft(_ - _) 结果为 -4, 执行步骤为:
  *   1- 2 = -1
  *   -1 - 3 = -4
  *
  * 对于 List(1, 2, 3).reduceRight(_ - _) 结果为2, 执行步骤为:
  *   2 - 3 = -1
  *   1- (-1) = 2
  */
val res1 = list.reduce(_ - _)
val res2 = list.reduceRight(_ - _)
println(res1)  // -4
println(res2)  // 2


/**
  * fold 操作 类似于 reduce 操作, 比 reduce 多一个初始值
  * fold 操作也分为 foldLeft 和 foldRight
  */
val res3 = list.fold(10)(_ * _)
println(res3)  // 10 * 1 * 2 * 3 = 60




















