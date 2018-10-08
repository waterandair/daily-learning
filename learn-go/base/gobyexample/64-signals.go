package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

// 使用 channel 处理信号
func main() {
	// 通过在 channel 上发送 os.Signal 值来进行信号通知。
	sigs := make(chan os.Signal, 1)
	done := make(chan bool, 1)

	// 为给定的 channel 注册指定的信号
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	// 阻塞的执行信号的接收，接收到后打印出来，并通知完成This goroutine executes a blocking receive for signals. When it gets one it’ll print it out and then notify the program that it can finish.
	go func() {
		sig := <-sigs
		fmt.Println()
		fmt.Println(sig)
		done <- true
	}()

	fmt.Println("awaiting signal")
	<-done
	fmt.Println("exiting")
}