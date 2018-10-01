package main

import "fmt"

func f(from string) {
	for i := 0; i < 3; i++ {
		fmt.Println(from, ":", i)
	}
}
func main() {
	f("direct")

	// 使用 go 关键字调用 goroutines
	go f("goroutine")

	// 也可以使用匿名函数运行 goroutines
	go func(msg string) {
		fmt.Println(msg)
	}("going")

	// 这两个函数是在不同的 goroutine 中异步执行的， 执行到此为止

	// Scanln 要求在程序退出之前按下一个键，这个等待是为了方便在控制台看到所有的程序输出
	fmt.Scanln()
	fmt.Println("done")
}