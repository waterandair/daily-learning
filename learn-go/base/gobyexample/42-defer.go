package main

import (
	"fmt"
	"os"
)

// defer 用于在程序最后执行，通常用于清理

func main() {
	f := creteFile("/tmp/defer.txt")
	defer closeFile(f)

	writeFile(f)
}

func creteFile(p string) *os.File {
	fmt.Println("creating")
	f, err := os.Create(p)
	if err != nil {
		panic(err)
	}
	return f
}

func writeFile(f *os.File) {
	fmt.Println("writing")
	fmt.Fprintln(f, "data")
}

func closeFile(f *os.File) {
	fmt.Println("closing")
	f.Close()
}
