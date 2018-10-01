package main

import (
	"fmt"
	"time"
)

// 可以使用 channel 处理不同的 goroutines 的同步执行
func worker(done chan bool) {
	fmt.Println("working...")
	time.Sleep(time.Second)
	fmt.Println("done")

	// 通知其他 goroutine 函数执行完成
	done <- true
}

func main() {
	done := make(chan bool)
	go worker(done)

	<-done
}
