package main

import "fmt"

func main() {

	// channel 是连接并发 goroutine 的管道。
	messages := make(chan string)

	go func() {messages <- "ping"}()

	// 默认情况下，发送和接收数据都是阻塞的，知道双方都做好准备
	msg := <- messages
	fmt.Println(msg)
}