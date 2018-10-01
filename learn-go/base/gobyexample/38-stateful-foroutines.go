package main

import (
	"fmt"
	"math/rand"
	"sync/atomic"
	"time"
)

// 上一节演示了使用 mutex 同步状态
// go 也可以使用 goroutine 和 channel 实现同步机制，这体现了go基于通信来共享内存，而不是通过共享内存去通信
// 实测比 mutex 快


// 在这个示例中， 状态 state 将由一个单独的 goroutine 管理
// 这可以保证数据永远不会被并发访问损坏
// 其他 goroutine 为了获取 state， 将向管理 state 的 goroutine 发送消息并接收相应回复

// 请求和相应的结构体
type readOp struct {
	key int
	resp chan int
}

type writeOp struct {
	key int
	val int
	resp chan bool
}


func main() {
	// 用来记录操作数
	var readOps uint64
	var writeOps uint64

	// reads 和 writes channel 是其他 goroutine 用来发送读写请求的
	reads := make(chan *readOp)
	writes := make(chan *writeOp)

	// 这个是管理状态的 goroutine，它重复的select reads 和 writes channel， 在请求到达时响应它们
	go func() {
		var state = make(map[int]int)
		for {
			select {
			case read := <-reads:
				// 处理读请求，给出响应
				read.resp <- state[read.key]
			case write := <-writes:
				// 处理写请求，给出响应
				state[write.key] = write.val
				write.resp <- true
			}
		}
	}()

	for r := 0; r < 100; r++ {
		go func() {
			for {
				// 构造一个读请求, 注意是指针
				read := &readOp{
					key: rand.Intn(5),
					resp: make(chan int),
				}

				// 发送读请求到 reads channel
				reads <- read
				// 阻塞等待响应
				<- read.resp
				// 收到响应后记录操作数
				atomic.AddUint64(&readOps, 1)
				time.Sleep(time.Millisecond)
			}
		}()
	}

	for w := 0; w < 10; w++ {
		go func() {
			for {
				// 构造一个写请求
				write := &writeOp{
					key: rand.Intn(5),
					val: rand.Intn(100),
					resp: make(chan bool),
				}
				// 将写请求发送给 writes channel
				writes <- write
				// 阻塞等待响应
				<- write.resp
				// 收到响应后记录操作数
				atomic.AddUint64(&writeOps, 1)
				time.Sleep(time.Millisecond)
			}
		}()
	}

	time.Sleep(time.Second)

	readOpsFinal := atomic.LoadUint64(&readOps)
	fmt.Println("readOps:", readOpsFinal)
	writeOpsFinal := atomic.LoadUint64(&writeOps)
	fmt.Println("writeOps:", writeOpsFinal)
}




