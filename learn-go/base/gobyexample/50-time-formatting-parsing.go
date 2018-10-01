package main

import (
	"fmt"
	"time"
)

// 格式化时间
func main() {
	p := fmt.Println

	t := time.Now()
	p(t.Format(time.RFC3339))  // 2018-10-01T17:57:53+08:00

	// 按照指定格式解析
	t1, _ := time.Parse(
		time.RFC3339,
		"2018-10-01T17:57:53+08:00")
	p(t1)  // 2018-10-01 17:57:53 +0800 CST

	// 转换为参数给出的格式
	p(t.Format("3:04PM"))  // 6:00PM
	p(t.Format("Mon Jan _2 15:04:05 2006"))  // Mon Oct  1 18:00:43 2018
	p(t.Format("2006-01-02T15:04:05.999999-07:00"))  // 2018-10-01T18:00:43.097916+08:00

	form := "3 04 PM"
	t2, e := time.Parse(form, "8 41 PM")
	p(t2)  // 0000-01-01 20:41:00 +0000 UTC

	// 2018-10-01T18:03:56-00:00
	fmt.Printf("%d-%02d-%02dT%02d:%02d:%02d-00:00\n",
		t.Year(), t.Month(), t.Day(),
		t.Hour(), t.Minute(), t.Second())

	ansic := "Mon Jan _2 15:04:05 2006"
	_, e = time.Parse(ansic, "8:41PM")
	p(e)
}
