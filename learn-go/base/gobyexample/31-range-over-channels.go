package main

import (
	"fmt"
	"time"
)

// channel 也可以使用 range 进行迭代

func main() {
	queue := make(chan string, 2)
	queue <- "one"
	queue <- "two"

	close(queue)  // 同一个goroutine中必须关闭channel， 否则会 fatal error: all goroutines are asleep - deadlock!

	//go func() {
	//	for elem := range queue {
	//		fmt.Println(elem)
	//	}
	//}()

	for elem := range queue {
		fmt.Println(elem)
	}

	time.Sleep(time.Second)
}
