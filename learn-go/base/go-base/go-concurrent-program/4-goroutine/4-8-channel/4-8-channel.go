package main

import (
	"fmt"
	"time"
)

/**
go 并发编程实战 代码清单 4-8  注意观察值类型和引用类型的区别， 与 4-7 对比
 */



/**
1. 运行观察结果

	The count map: map[Count:{0}]. [sender]
	The count map: map[Count:{0}]. [sender]
	The count map: map[Count:{0}]. [sender]
	The count map: map[Count:{0}]. [sender]
	The count map: map[Count:{0}]. [sender]
	Stopped. [receiver]


2. 改变 mapChan 和 countMap 的声明并执行，观察结果
	var mapChan = make(chan map[string]*Counter, 1)
	countMap := map[string]*Counter {
		"Count"； &Counter{},
	}

	The count map: map[Count:{count: 1}]. [sender]
	The count map: map[Count:{count: 2}]. [sender]
	The count map: map[Count:{count: 3}]. [sender]
	The count map: map[Count:{count: 4}]. [sender]
	The count map: map[Count:{count: 5}]. [sender]
	Stopped. [receiver]


 */

// 计数器类型
type Counter struct {
	count int
}

func (counter *Counter) String() string {
	return fmt.Sprintf("{count: %d}", counter.count)
}

var mapChan = make(chan map[string]Counter, 1)
// var mapChan = make(chan map[string]*Counter, 1)

func main() {
	syncChan := make(chan struct{}, 2)

	// 接收
	go func() {
		for {
			if elem, ok := <-mapChan; ok {
				counter := elem["Count"]
				counter.count ++
			} else {
				break
			}
		}

		fmt.Println("Stopped. [receiver]")
		syncChan <- struct{}{}
	}()

	// 发送
	go func() {
		countMap := map[string]Counter {
			"Count": Counter{},
		}

		//countMap := map[string]*Counter {
		//	"Count": &Counter{},
		//}


		for i := 0; i < 5; i++ {
			mapChan <- countMap
			time.Sleep(time.Millisecond)
			fmt.Printf("The count map: %v. [sender]\n", countMap)
		}
		close(mapChan)
		syncChan <- struct{}{}
	}()

	<- syncChan
	<- syncChan
}
