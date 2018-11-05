package main

import (
	"fmt"
	"time"
)

/**
标准库中的 time 包中的一些 API 使用 channel 辅助实现的

timer 对外通知定时器到期的途径就是 channel，有字段 C 表示
 */
func main() {
	timer := time.NewTimer(2 * time.Second)
	fmt.Printf("present time: %v. \n", time.Now())
	expirationTime := <-timer.C
	fmt.Println("expiration time: ", expirationTime)
	fmt.Println("stop timer: ", timer.Stop())
}

/**

present time: 2018-11-03 16:03:41.426478897 +0800 CST m=+0.000321760.
expiration time:  2018-11-03 16:03:43.426577884 +0800 CST m=+2.000420817
stop timer:  false
 */