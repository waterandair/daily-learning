package main

import (
	"fmt"
	"os"
)

type point struct {
	x, y int
}

func main() {
	p := point{1, 2}

	//{1 2}
	fmt.Printf("%v\n", p)

	// {x:1 y:2}
	fmt.Printf("%+v\n", p)

	// main.point{x:1, y:2}
	fmt.Printf("%#v\n", p)

	// main.point  打印数据类型用 %T
	fmt.Printf("%T\n", p)

	// true 格式化bool值
	fmt.Printf("%t\n", true)

	// 123
	fmt.Printf("%d\n", 123)

	// 1110  二进制
	fmt.Printf("%b\n", 14)

	// ！ 打印对应的字符
	fmt.Printf("%c\n", 33)

	// 1c8 十六进制
	fmt.Printf("%x\n", 456)

	// 78.900000
	fmt.Printf("%f\n", 78.9)

	// 1.234000e+08
	fmt.Printf("%e\n", 123400000.0)
	// 1.234000E+08
	fmt.Printf("%E\n", 123400000.0)

	// "string" 基础的格式化字符串
	fmt.Printf("%s\n", "\"string\"")

	// "\"string\""  打印出双引号
	fmt.Printf("%q\n", "\"string\"")

	// 6865782074686973
	fmt.Printf("%x\n", "hex this")

	// 打印指针
	fmt.Printf("%p\n", &p)

	// |    12|   345|
	fmt.Printf("|%6d|%6d|\n", 12, 345)

	// |1.20  |3.45  |
	fmt.Printf("|%-6.2f|%-6.2f|\n", 1.2, 3.45)

	// |   foo|     b|
	fmt.Printf("|%6s|%6s|\n", "foo", "b")

	// |foo   |b     |
	fmt.Printf("|%-6s|%-6s|\n", "foo", "b")

	// sprintf 返回一个字符串，而不是打印
	s := fmt.Sprintf("a %s", "string")
	fmt.Println(s)

	fmt.Fprintf(os.Stderr, "an %s\n", "error")

}
