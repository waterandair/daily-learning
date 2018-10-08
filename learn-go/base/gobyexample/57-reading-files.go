package main

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"os"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}
func main() {
	// 全部内容读入内存
	dat, err := ioutil.ReadFile("/tmp/dat1")
	check(err)
	fmt.Print(string(dat))

	f, err := os.Open("/tmp/dat1")
	check(err)
	defer f.Close()

	b1 := make([]byte, 5)
	n1, err := f.Read(b1)  // 返回读取到的字节数
	check(err)
	fmt.Printf("%d bytes: %s\n", n1, string(b1))  // 5 bytes: hello

	// 指定位置读
	o2, err := f.Seek(6, 0)
	check(err)
	b2 := make([]byte, 2)
	n2, err := f.Read(b2)
	check(err)
	fmt.Printf("%d bytes @ %d: %s\n", n2, o2, string(b2))  // 2 bytes @ 6: go

	// io 包提供的一些功能，同上
	o3, err := f.Seek(6, 0)
	check(err)
	b3 := make([]byte, 2)
	n3, err := io.ReadAtLeast(f, b3, 2)
	check(err)
	fmt.Printf("%d bytes @ %d: %s\n", n3, o3, string(b3))

	// seek 可以是当前文件的指针指回已经读取过的位置
	_, err = f.Seek(0, 0)

	// 缓冲读取器, 可以用于提升读取小文件的效率
	r4 := bufio.NewReader(f)
	b4, err := r4.Peek(5)
	check(err)
	fmt.Printf("5 bytes: %s \n", string(b4))
}


