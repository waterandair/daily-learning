package main

import (
	"fmt"
	"time"
)

var strChan = make(chan string, 3)

func main() {
	syncChan1 := make(chan struct{}, 1)
	syncChan2 := make(chan struct{}, 2)
	go receive(strChan, syncChan1, syncChan2)
	go send(strChan, syncChan1, syncChan2)

	<-syncChan2
	<-syncChan2
}

func receive(strChan <-chan string, syncChan1 <-chan struct{}, syncChan2 chan<- struct{}) {
	// 阻塞等待发送方发送
	<-syncChan1
	fmt.Println("received a sync signal and wait a second... [receive]")
	time.Sleep(time.Second)
	for elem := range strChan {
		fmt.Println("received: ", elem, "[receiver]")
	}
	fmt.Println("stopped. [receiver]")
	// 通知主 goroutine 接收完成
	syncChan2 <- struct{}{}
}

func send(strChan chan<- string, syncChan1 chan<- struct{}, syncChan2 chan<- struct{} ) {

	for _, elem := range []string{"a", "b", "c", "d"} {
		strChan <- elem
		fmt.Println("wait 2 seconds...[sender]")
		if elem == "c" {
			syncChan1 <- struct{}{}
			fmt.Println("wait a sync signal.[sender]")
		}
	}

	fmt.Println("wait 2s[sender]")
	close(strChan)
	syncChan2 <- struct{}{}
}