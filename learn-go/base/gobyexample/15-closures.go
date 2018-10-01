package main

import "fmt"

// go 语言支持匿名函数，可以实现闭包
func intSeq() func() int {
	i := 0
	return func() int {
		i++
		return i
	}
}
func main() {
	nextInt := intSeq()

	fmt.Println(nextInt())
	fmt.Println(nextInt())
	fmt.Println(nextInt())

	newInts := intSeq()
	fmt.Println(newInts())
}
