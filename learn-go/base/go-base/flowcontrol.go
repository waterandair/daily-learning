package main

import (
	"fmt"
	"math"
	"runtime"
	"time"
	"os"
)

func main() {
	//forDemo1()
	//forDemo2()
	//
	//ifDemo(2)
	//ifDemo2(2, 2, 5)
	//ifDemo3(2, 3, 5)
	//
	// switchDemo()
	// switchDemo2()
	//
	// deferDemo()
	// fmt.Println(deferDemo2())

	// gotoDemo()

	// 变参
	// multiParams(1, 2, 3)

	// 抛出错误, 进入"恐慌"
	// panicDemo()

	// 让进入恐慌状态的 goroutine 恢复回来
	// fmt.Println(recoverDemo(panicDemo))

	/*
	go 在流程控制方便的特点：
		没有 do 和 while 循环， 只有一个更广义的 for 语句
		switch 语句灵活多变， 还可以用于类型判断
		if 语句和 switch 语句都可以只包含一条初始化子语句
		break 语句和 continue 语句可以后跟一条标签(label)语句，以标识需要终止或继续的代码块
		defer 语句可以更加方便的执行异常捕获和资源回收任务
		select 语句也用于多分支选择，但至于通道配合使用
		go 语句用于异步启用 goroutine 并指定执行函数
	 */

}

func forDemo1() {
	sum := 0
	for i := 0; i < 10; i++ {
		sum ++
	}
	fmt.Println(sum)
}

// for 是 Go 的 "while"
func forDemo2() {
	sum := 1
	for sum <= 10 {
		sum += sum
	}
	fmt.Println(sum)
}

/* range
range 表达式一般只会在迭代开始前被求值一次
针对 range 表达式的不同结果，range 子句的行为也会不同，

range 表达式的类型    	   |   		第一个产出值        |  第二个产出值   			       | 备注
a: [n]E, *[n]E, []E	   | i: int 类型的元素索引值     | 与索值对应的元素的值a[i],          | a 为range 表达式结果值，n为数据类型的长度，E为数组类型或切片类型的元素类型
												  类型为 E
------------------------------------------------------------------------------------------------------
s: string 类型          | i: int 类型的元素索引值     | 与索引对应的元素的值，              | s 为 range 表达式的结果值
											      类型为 rune
----------------------------------------------------------------------------------------------------------
m: map[K]V			   | k: 键值 类型为 K			  | 与键对应的元素值 m[K], 类型为 V     | m 为 range 表达式的结果值，K为字典的键的类型，V 为字典的元素类型
-----------------------------------------------------------------------------------------------------------------
c: chan E 或 <- chan E  | e: 元素的值，类型为 E       |                                 | c 为 range 表达式的结果值，E为通道的元素的类型
																				      注意: 迭代为 nil 的通道会让当前流程永远阻塞在 for 语句上
*/
func forDemo3() {
	ints := [4]int{1, 2, 3, 4}
	for i, d := range ints {
		fmt.Println(i, d)
	}
}

// 死循环
func forEndLess() {
	for {

	}
}


func ifDemo(x float64){
	if x < 0 {
		ifDemo(-x)
	}
	fmt.Println(math.Sqrt(x))
}

// if 的便捷语句: if 语句可以在条件之前执行一个简单的语句,这个语句定义的变量的作用域仅在 if 范围内
func ifDemo2(x, n, lim float64) {
	if v:= math.Pow(x, n); v < lim {
		fmt.Println(v)
		return
	}
	fmt.Println(lim)
}

func ifDemo3(x, n, lim float64) {
	if v:= math.Pow(x, n); v < lim {
		fmt.Println(v)
	} else {
		// if 快捷语句定义的变量可以在对应的 else 块中使用
		fmt.Printf("%g >= %g \n", v, lim)
	}
	fmt.Println(lim)
}

func switchDemo() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		fmt.Printf("%s.", os)
	}
}

// 没有条件的 switch 同 'switch true' 一样, 这一构造是的可以用更清晰的形式来编写长的 if-then-else 链
func switchDemo2() {
	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("morning")
	case t.Hour() < 17:
		fmt.Println("afternoon")
	default:
		fmt.Println("Good evening")
	}
}

// fallthrough 示例
func switchDemo3() {
	switch lang:= "python"; lang {
	case "Ruby":
		fallthrough  // fallthrough 表示向下一个 case 语句转移流程控制权， 这段代码表示变量 lang 为 “ruby” 或 “python” 时执行打印
	case "python":
		fmt.Println("interpreted language")
	case "c", "java", "go":
		fmt.Println("compiled language")
	default:
		fmt.Println("unknown")
	}
}

// 类型 switch 语句, fallthrough 语句不允许出现在类型 switch 语句中
func switchDemo4() {
	var v interface{}

	switch v.(type) {
	case string:
		fmt.Println("string")
	case int, uint, int8:
		fmt.Println("int")
	default:
		fmt.Println("unsupported value")
	}
}

// 延迟函数的执行知道上层函数返回, 延迟调用的参数会立即生成, 但是在上层函数返回前的函数都不会被调用
func deferDemo() {
	defer fmt.Println("world")
	fmt.Print("hello ")
}

// 延迟的函数调用被压入一个栈中。当函数返回时， 会按照后进先出的顺序调用被延迟的函数调用。
func deferDemo2() int {
	a, b := 1, 2
	fmt.Println("Start")
	for i := 0; i < 3; i++ {
		defer fmt.Println(i)
	}
	fmt.Println("End")
	return a + b
}

func gotoDemo() {
	i := 0
	Here:
		fmt.Println(i)
		i ++
		if i > 10 {
			return
		}
		// 标签大小写敏感
		goto Here
}

func multiParams(arg ... int) {
	for _, v := range arg {
		fmt.Println(v)
	}
}

func panicDemo()  {
	var user = os.Getenv("USER")
	if user == "" {
		panic("no value for $USER")
	}

}

// 检查传入的函数在执行时是否产生了 panic
func recoverDemo(f func()) (b bool){
	defer func() {
		if x:= recover(); x != nil {
			b = true
		}
	}()
	f()
	return
}
