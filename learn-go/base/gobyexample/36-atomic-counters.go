package main

import (
	"fmt"
	"sync/atomic"
	"time"
)

// go 中主要使用 channel 通信进行状态管理，但是也有其他的方式
// 下面使用 sync/atomic 包实现多个 goroutines 的原子计数器

func main() {
	// 使用无符号的正整数表示计数器
	var ops uint64

	for i := 0; i < 50; i++ {
		go func() {
			for {
				atomic.AddUint64(&ops, 1)
				time.Sleep(time.Millisecond)
			}
		}()
	}

	// 等待一秒钟
	time.Sleep(time.Second)
	// 为了让计数操作在其他 goroutine 中继续正常进行，这里使用 atomic 提供的 LoadUint64 取出当前的值
	opsFinal := atomic.LoadUint64(&ops)
	fmt.Println(opsFinal)
}
