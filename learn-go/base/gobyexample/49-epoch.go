package main

import (
	"fmt"
	"time"
)

func main() {
	// 时间戳
	now := time.Now()
	secs := now.Unix()  // 秒
	nanos := now.UnixNano()  // 纳秒
	// 毫秒数需要自己计算
	mills := nanos / 1000000

	fmt.Println(now)  // 2018-10-01 17:55:39.16434731 +0800 CST m=+0.000237526
	fmt.Println(secs)  // 1538387739
	fmt.Println(mills)  // 1538387739164
	fmt.Println(nanos)  // 1538387739164347310

	// 将秒或纳秒转换为时间
	fmt.Println(time.Unix(secs, 0))  // 2018-10-01 17:55:39 +0800 CST
	fmt.Println(time.Unix(0, nanos))  // 2018-10-01 17:55:39.16434731 +0800 CST
}
