package main

import "fmt"

func main() {
	// 默认情况下，channel 是没有缓冲，这意味着要有相应的接收方时才可以发送。
	// 有缓冲的 channel 不需要相应的接收放，就可以发送成功
	messages := make(chan string, 2)

	messages <- "buffered"
	messages <- "channel"

	fmt.Println(<-messages)
	fmt.Println(<-messages)
}
