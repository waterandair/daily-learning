package main

import "fmt"

/**
	下面代码中， 接收方先阻塞， 等待发送放发送完数据并关闭 channel 后才开始接收数据

		注意： 一定不要在接收方关闭channel，同一个 channel 只能关闭一次

		接收方可以用第二个参数 判断通道是否已关闭

 */
func main() {
	// 用于发送数据
	dataChan := make(chan int, 5)
	// 用于同步阻塞
	syncChan1 := make(chan struct{}, 1)
	syncChan2 := make(chan struct{}, 2)

	// 接收
	go func() {
		// 阻塞等待发送方发送完数据
		<-syncChan1

		for {
			if elem, ok := <- dataChan; ok {
				fmt.Printf("Received: %d [receiver]\n", elem)
			} else {
				break
			}
		}

		fmt.Println("Done. [receiver]")
		syncChan2 <- struct{}{}
	}()

	// 发送
	go func() {
		for i := 0; i < 5; i++ {
			dataChan <- i
			fmt.Printf("Sent: %d [sender]\n", i)
		}
		close(dataChan)

		syncChan1 <- struct{}{}

		fmt.Println("Done. [sender]")
		syncChan2 <- struct{}{}
	}()

	<- syncChan2
	<- syncChan2
}
