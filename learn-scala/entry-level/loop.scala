// while
var i = 3
while (i>0) {
  i -= 1
  printf("i is %d\n", i)
}

// do-while
i = 0
do {
  i += 1
  println(i)
}while (i < 3)

// for (变量 <- 表达式) 语句块;  其中, "变量 <- 表达式" 被称为"生成器(generator)"
for (i <- 1 to 3) println(i)
for (i <- 1 to 5 by 2) println(i)

// 过滤一些满足定制条件的结果,需要使用到称为"守卫(guard)"的表达式
for  (i <- 1 to 5 if i%2==0) println(i)
println("----------------------------")

// scala 支持"多个生成器"的情形, 可以用分号把它们隔开
for (i <- 1 to 3; j <- 1 to 3) println(i*j)

// for 推导式 采用 yield 关键字
for (i <- 1 to 5 if i%2==0) yield i


