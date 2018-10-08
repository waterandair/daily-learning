package main

import (
	"flag"
	"fmt"
)

// ./60-command-line-flags -word=opt -numb=7 -fork -svar=flag
func main() {
	// 定义命名的参数和默认值，说明  在命令后输入 -h， 会打印出定义好的使用说明
	wordPtr := flag.String("word", "foo", "a string")
	numbPtr := flag.Int("numb", 42, "an int")
	boolPtr := flag.Bool("fork", false, "a bool")

	var svar string
	flag.StringVar(&svar, "svar", "bar", "a string var")
	flag.Parse()

	fmt.Println("word:", *wordPtr)  // word: opt
	fmt.Println("numb:", *numbPtr)  // numb: 7
	fmt.Println("fork:", *boolPtr)  // fork: true
	fmt.Println("svar:", svar)  // svar: flag
	// 没有名称的参数
	fmt.Println("tail:", flag.Args())  // tail: []


}
