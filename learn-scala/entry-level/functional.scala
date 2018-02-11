/**
  * 定义函数
  * scala 要求必须给出所有参数的类型,但是不一定给出函数返回值的类型,
  * 只要右侧的函数体中不包含递归的语句,scala 就可以自己根据右侧的表达式推断出返回类型
   */
def counter(value: Int): Int = { value + 1}
// or
val counter2:Int => Int = {(value:Int) => value + 1}
println(counter2(1))

// 默认参数
def sayHello(firstName: String, middleName: String = "大胡子", lastName: String = "哈登" ) = firstName + middleName + lastName


// 在调用函数时,也可以不按照函数定义的参数顺序来传递参数,而是使用带名参数的方式来传递,
sayHello(firstName = "科比", lastName = "布莱恩特", middleName = "专治不服")

// 还可以混用未命名参数和带名参数,但是未命名参数必须排在带名参数前面
sayHello("科比", lastName = "布莱恩特", middleName = "曼巴")

// 变长参数
def sum(nums: Int*) = {
  var res = 0
  for (num <- nums) res += num
  res
}
println(sum(1, 2, 3, 4, 5))

// 使用序列调用变长参数
val s = sum(1 to 5: _ *)
println(s)
// 使用递归实现累加
def sum2(nums: Int*): Int = {
  if (nums.length == 0) 0
  else nums.head + sum2(nums.tail: _*)
}
println(sum2(1, 2, 3, 4, 5))
println("*"*30)

/**
  * 过程
  * 在 scala 中,定义函数时,如果函数体直接包裹在了花括号里面,而没有使用 = 连接, 则函数的返回值类型就是 Unit.
  * 过程通常用于不需要返回值的函数
  * 定义过程还有一种写法, 就是将函数的返回值类型定义为 Unit
  */
def sayHello2(name: String): Unit = "hello," + name


/**
  * 闭包
  */
def plusStep(step: Int) = (num: Int) => num + step
val myFunc = plusStep(3)
val myFunc2 = plusStep(4)
println(myFunc(10))
println(myFunc2(10))
println("-"*30)

/**
  * 高阶函数
  * 一个接受其他函数作为参数或者返回一个函数的函数就是高阶函数
  * 下面的函数是从a到b的f(n)的累加形式(a <= n <= b), 唯一的区别就是各种场景下f(n)的具体实现不同
  */
// 计算给定两个数区间中的所有整数的和
def sum(f: Int => Int, a: Int, b: Int): Int = {
  if (a>b) 0 else f(a) + sum(f, a+1, b)
}
def self(x: Int): Int = x  // 只需要修改这里,就可以实现连续整数平方和或者连续整数关于2的幂次和
def square(x: Int): Int = x * x
def powerOfTwo(x: Int): Int = if(x == 0) 1 else 2 * powerOfTwo(x-1)
def sumInts(a: Int, b: Int): Int = sum(self _, a, b)
def sumSquared(a: Int, b: Int): Int = sum(square _, a, b)
def sumPowersOfTwo(a: Int, b: Int): Int = sum(powerOfTwo _, a, b)
println(sumInts(1, 3))
println(sumSquared(1, 3))
println(sumPowersOfTwo(1, 3))
println("-"*30)

/**
  * 占位符语法
  * 为了让函数字面量更加简洁,可以使用下划线作为一个或多个参数的占位符,只要每个参数在函数字面量内仅出现一次
  */
val numList = List(-3, -5, 1, 6, 9)
numList.filter(x => x > 0)
numList.filter(_ > 0)


/**
  * curring 函数
  * 指的是将原来接受两个参数的一个函数,转换为两个函数,第一个函数接受原先的第一个参数,然后返回接受原先第二个参数的第二个函数
  * 再函数调用的过程中,就变为了两个函数连续调用的形式
  *
   */
def sum(a: Int, b:Int) = a + b
def sum2(a:Int) = (b:Int) => a + b
def sum3(a: Int)(b: Int) = a + b

/**
  * Scala中，不需要使用return来返回函数的值，函数最后一行语句的值，就是函数的返回值。
  * 在Scala中，return用于在匿名函数中返回值给包含匿名函数的带名函数，并作为带名函数的返回值。
  * 使用return的匿名函数，是必须给出返回类型的，否则无法通过编译
  */





