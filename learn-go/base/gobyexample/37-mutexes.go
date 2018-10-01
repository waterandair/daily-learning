package main

import (
	"fmt"
	"math/rand"
	"sync"
	"sync/atomic"
	"time"
)

// 对于复杂的状态管理，可以使用 mutexes

func main() {
	// 使用 map 存储状态
	var state = make(map[int]int)

	// 这个互斥锁将同步访问 state
	var mutex = &sync.Mutex{}

	// 记录读写操作的数量
	var readOps uint64
	var writeOps uint64

	// 100 个 goroutine 读取状态
	for r := 0; r < 100; r++ {
		go func() {
			total := 0
			for {
				key := rand.Intn(5)
				// 读取前加锁
				mutex.Lock()
				total += state[key]
				// 读取后解锁
				mutex.Unlock()
				// 记录读取的次数
				atomic.AddUint64(&readOps, 1)

				time.Sleep(time.Millisecond)
			}
		}()
	}

	// 10 个 goroutine 修改状态
	for w := 0; w < 10; w++ {
		go func() {
			for {
				key := rand.Intn(5)
				val := rand.Intn(100)
				// 修改前加锁
				mutex.Lock()
				state[key] = val
				// 修改后解锁
				mutex.Unlock()
				// 计数
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

	mutex.Lock()
	fmt.Println("state:", state)
	mutex.Unlock()

}
