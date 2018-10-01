package main

import (
	"fmt"
	"time"
)

func main() {
	p := fmt.Println

	now := time.Now()
	p(now)  // 2018-10-01 17:43:04.328833046 +0800 CST m=+0.000252954

	then := time.Date(2018, 10, 1, 17, 39, 58,651387237, time.UTC )
	p(then)  // 2018-10-01 17:39:58.651387237 +0000 UTC

	// 时间戳
	timestamp := time.Now().Unix()
	p(timestamp)  // 1538387091

	p(then.Year())
	p(then.Month())
	p(then.Day())
	p(then.Hour())
	p(then.Minute())
	p(then.Second())
	p(then.Nanosecond())
	p(then.Location())
	p(then.Weekday())

	p(then.Before(now))
	p(then.After(now))
	p(then.Equal(now))

	diff := now.Sub(then)
	p(diff)  // -7h53m53.279469451s

	p(diff.Hours())  // -7.887588635905278
	p(diff.Minutes())  // -473.2553181543167
	p(diff.Seconds())  // -28395.319089259
	p(diff.Nanoseconds())  // -28395319089259

	p(then.Add(diff))
	p(now.Equal(then.Add(diff)))  // true
}
