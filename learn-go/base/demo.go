package main

import (
	"path/filepath"
	"os/exec"
	"os"
	"fmt"
)

func main() {
	// 获取正确的可执行文件路径
	file, err := exec.LookPath(os.Args[0])
	if err != nil{
		fmt.Println(err)
	}
	path, err := filepath.Abs(file)
	fmt.Println(path)
}
