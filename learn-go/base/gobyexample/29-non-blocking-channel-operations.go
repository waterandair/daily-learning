package main

import (
	"fmt"
)

// 默认情况下， channel 是阻塞的，但是可以使用 select 的 default 项实现非阻塞的 channel

func main() {
	messages := make(chan string)
	signal := make(chan bool)

	select {
	case msg := <- messages:
		fmt.Println("received message", msg)
	default:
		fmt.Println("no message received")
	}

	msg := "hi"
	select {
	// 这里 msg 不能发送到 channel， 因为 channel 既没有缓冲区，也没有接收器，因此执行 default
	case messages <- msg:
		fmt.Println("sent message", msg)
	default:
		fmt.Println("no message sent")
	}

	// 可以使用 select 进行多路非阻塞选择
	select {
	case msg := <-messages:
		fmt.Println("received message", msg)
	case sig := <-signal:
		fmt.Println("received signal", sig)
	default:
		fmt.Println("no activity")
	}
}
