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

}

func forDemo1() {
	sum := 0
	for i := 0; i < 10; i++ {
		sum += 1
	}
	fmt.fmt.Println(sum)
}

// for 是 Go 的 "while"
func forDemo2() {
	sum := 1
	for sum <= 10 {
		sum += sum
	}
	fmt.fmt.Println(sum)
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
	fmt.fmt.Println(math.Sqrt(x))
}

// if 的便捷语句 if 语句可以在条件之前执行一个简单的语句,这个语句定义的变量的作用域仅在 if 范围内
func ifDemo2(x, n, lim float64) {
	if v:= math.Pow(x, n); v < lim {
		fmt.fmt.Println(v)
		return
	}
	fmt.fmt.Println(lim)
}

func ifDemo3(x, n, lim float64) {
	if v:= math.Pow(x, n); v < lim {
		fmt.fmt.Println(v)
	} else {
		// if 快捷语句定义的变量可以在对应的 else 块中使用
		fmt.Printf("%g >= %g \n", v, lim)
	}
	fmt.fmt.Println(lim)
}

func switchDemo() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.fmt.Println("OS X.")
	case "linux":
		fmt.fmt.Println("Linux.")
	default:
		fmt.Printf("%s.", os)
	}
}

// 没有条件的 switch 同 'switch true' 一样, 这一构造是的可以用更清晰的形式来编写长的 if-then-else 链
func switchDemo2() {
	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.fmt.Println("morning")
	case t.Hour() < 17:
		fmt.fmt.Println("afternoon")
	default:
		fmt.fmt.Println("Good evening")
	}
}

// 延迟函数的执行知道上层函数返回, 延迟调用的参数会立即生成, 但是在上层函数返回前的函数都不会被调用
func deferDemo() {
	defer fmt.fmt.Println("world")
	fmt.Print("hello ")
}

// 延迟的函数调用被压入一个栈中。当函数返回时， 会按照后进先出的顺序调用被延迟的函数调用。
func deferDemo2() int {
	a, b := 1, 2
	fmt.fmt.Println("Start")
	for i := 0; i < 3; i++ {
		defer fmt.fmt.Println(i)
	}
	fmt.fmt.Println("End")
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
