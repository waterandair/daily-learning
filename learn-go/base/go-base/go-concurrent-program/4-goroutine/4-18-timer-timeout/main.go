package main

import (
	"fmt"
	"time"
)

/**
用 timer 可以简单实现定时器，
除了使用 timer 的 C 字段，还可以直接使用 time.After(time.Millisecond * 500)
 */
func main() {
	intChan := make(chan int, 1)
	go func() {
		// 阻塞 1s
		time.Sleep(time.Second)
		intChan <- 1
	}()

	select {
	case e:= <-intChan:
		fmt.Printf("received: %v\n", e)
	case <-time.NewTimer(time.Millisecond * 500).C:
		fmt.Println("Timeout")
	}
}
