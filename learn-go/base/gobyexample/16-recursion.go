package main

import "fmt"

// 递归
// 阶乘
func fact(n int) int {
	if n == 0 {
		return 1
	}

	return n * fact(n-1)
}

// 斐波那契
func fib(n int) int {
	if n == 0 {
		return 0
	}
	if n == 1 || n == 2 {
		return 1
	}

	return fib(n-1) + fib(n-2)
}

// 斐波那契循环

func fib2(n int) int {
	i, a, b := 0, 0, 1

	for i < n {
		a, b = b, a + b
		i ++
	}
	return a
}
func main() {
	fmt.Println(fact(4))

	fmt.Println(fib(4))
	fmt.Println(fib2(4))
}
