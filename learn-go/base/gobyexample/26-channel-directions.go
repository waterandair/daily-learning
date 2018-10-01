package main

import "fmt"

// channel 作为函数参数的时候，可以指定 channel 是仅发送或仅接收, 这可以增加程序的安全性

// ping 只发送
func ping(pings chan<- string, msg string) {
	pings <- msg
}

// 只接收
func pong(pings <-chan string, pongs chan<- string) {
	msg := <-pings
	pongs <- msg
}

func main() {
	pings := make(chan string, 1)
	pongs := make(chan string, 1)

	ping(pings, "passed message")
	pong(pings, pongs)

	fmt.Println(<-pongs)

}
