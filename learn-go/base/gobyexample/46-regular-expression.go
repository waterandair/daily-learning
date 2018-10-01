package main

import (
	"bytes"
	"fmt"
	"regexp"
)

func main() {
	// 测试匹配 regexp.MatchString
	match, _ := regexp.MatchString("p([a-z]+)ch", "peach")
	fmt.Println(match)  // true

	// 构造正则
	r, _ := regexp.Compile("p([a-z]+)ch")

	// 匹配
	fmt.Println(r.MatchString("peach"))  // true
	fmt.Println(r.Match([]byte("peach"))) // true

	// 查找字符串
	fmt.Println(r.FindString("peach punch"))  // peach

	// 查找第一个符合的字符串的 开始和结束 的索引 [0, 5)
	fmt.Println(r.FindStringIndex("peach punch"))  // [0 5]

	// 返回完整匹配和局部匹配
	fmt.Println(r.FindStringSubmatch("peach punch"))  // [peach ea]

	// 返回完整匹配和局部匹配的索引
	fmt.Println(r.FindStringSubmatchIndex("peach punch"))  // [0 5 1 3]

	// 返回所有匹配的字符串
	fmt.Println(r.FindAllString("peach punch pinch", -1))  // [peach punch pinch]

	// 返回所有完整匹配和局部匹配的字符串 的索引
	// [[0 5 1 3] [6 11 7 9] [12 17 13 15]]
	fmt.Println(r.FindAllStringSubmatchIndex("peach punch pinch", -1))

	// 返回指定数目的匹配
	fmt.Println(r.FindAllString("peach punch pinch", 2))  // [peach punch]

	// 区别 regexp.Compile， MustCompile 只有一个返回值
	r = regexp.MustCompile("p([a-z]+)ch")
	fmt.Println(r)  // p([a-z]+)ch

	fmt.Println(r.ReplaceAllString("a peach", "<fruit>"))

	in := []byte("a peach")
	out := r.ReplaceAllFunc(in, bytes.ToUpper)
	fmt.Println(string(out))  // a PEACH
}
