package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// 行过滤器是一种常见的程序，它读取 stdin 上的输入，处理后将结果打印到 stdout。
// grep sed 是常见的行过滤器

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		ucl := strings.ToUpper(scanner.Text())
		fmt.Println(ucl)
	}

	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}
