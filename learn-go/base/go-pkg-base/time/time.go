package main

import (
	"fmt"
	"time"
)

func main() {

	now := time.Now()
	fmt.Println(now)
	// 星期
	week := time.Now().Weekday()
	fmt.Println(week)
}
