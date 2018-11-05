package main

import (
	"fmt"
	"time"
)

var mapChan2 = make(chan map[string]int, 1)

/**
观察 map类型 在 chan 传递中传递的是引用
 */
func main() {
	syncChan := make(chan struct{}, 2)
	// 接收
	go func() {
		for {
			if elem, ok := <-mapChan2; ok {
				elem["count"] ++
			} else {
				break
			}
		}

		fmt.Println("Stopped. [receiver]")
		syncChan <- struct{}{}
	}()

	// 发送
	go func() {
		countMap := make(map[string]int)

		for i := 0; i < 5; i++ {
			mapChan2 <- countMap
			time.Sleep(time.Millisecond)
			fmt.Printf("The count map: %v. [sender]\n", countMap)
		}

		close(mapChan2)

		syncChan <- struct{}{}
	}()

	<-syncChan
	<-syncChan
}

/**
The count map: map[count:1]. [sender]
The count map: map[count:2]. [sender]
The count map: map[count:3]. [sender]
The count map: map[count:4]. [sender]
The count map: map[count:5]. [sender]
Stopped. [receiver]
 */
