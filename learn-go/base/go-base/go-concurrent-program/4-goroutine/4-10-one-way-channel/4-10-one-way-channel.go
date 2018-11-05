package main

import (
	"fmt"
	"time"
)

/**
	channel 可以是单向的，一般不会在初始化的时候设置为单向，那样就没有意义了
	一般会初始化一个 双向channel ， 然后在函数定义中接收 单向channel 类型，
	这样，就可以在语言层面，保证 channel 在函数中的安全性，只可以发送或删除
*/

var strChan = make(chan string, 3)

func main() {
	syncChan1 := make(chan struct{}, 1)
	syncChan2 := make(chan struct{}, 2)

	// 接收
	go receive(strChan, syncChan1, syncChan2)
	// 发送
	go send(strChan, syncChan1, syncChan2)

	// 等待发送和接收方都完成
	<- syncChan2
	<- syncChan2

}

/**
接收方
	注意函数定义的时候，channel类型均为单向的，这就规定了 channel 在函数中的操作只能是接收或发送
*/
func receive(strChan <-chan string, syncChan1 <-chan struct{}, syncChan2 chan<- struct{}) {
	// 只能接收， 等待发送发通知可以开始接收
	<- syncChan1
	fmt.Println("received a sync signal and wait a second... [receiver]")
	time.Sleep(time.Second)

	for {
		if elem, ok := <-strChan; ok {
			fmt.Println("received:", elem, "[receiver]")
		} else {
			break
		}
	}

	fmt.Println("stopped. [receiver]")

	// 通知主线程， 接收端接收完毕
	syncChan2 <- struct{}{}
}

/**
发送方
 */
func send(strChan chan<- string, syncChan1 chan<- struct{}, syncChan2 chan<- struct{}) {
	for _, elem := range []string{"a", "b", "c", "d"} {
		strChan <- elem
		fmt.Println("Sent:", elem, "[sender]")

		if elem == "c" {
			// 通知 接收方可以开始接收
			syncChan1 <- struct{}{}
			fmt.Println("sent a sync signal. [sender]")
		}
	}

	fmt.Println("wait 2 seconds... [sender]")
	time.Sleep(time.Second * 2)
	close(strChan)

	// 通知主线程 发送方发送完毕
	syncChan2 <- struct{}{}
}
