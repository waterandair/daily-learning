package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"os"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	// 向文件直接写入字符串
	d1 := []byte("hello\ngogo\n")
	err := ioutil.WriteFile("/tmp/dat1", d1, 0644)
	check(err)

	// 做更多精细的操作，需要打开文件流
	f, err := os.Create("/tmp/dat2")
	check(err)
	defer f.Close()  // 打开文件后立即使用 defer 关闭， 是良好的习惯

	d2 := []byte{115, 111, 109, 101, 10}
	n2, err := f.Write(d2)  // 返回写入的字节数
	check(err)
	fmt.Printf("wrote %d bytes\n", n2)  // wrote 5 bytes

	n3, err := f.WriteString("writes\n")  // worte 7 bytes
	fmt.Printf("worte %d bytes\n", n3)

	f.Sync()  // 写入硬盘


	// 缓冲写入器
	w := bufio.NewWriter(f)
	n4, err := w.WriteString("bufferd\n")
	fmt.Printf("wrote %d bytes\n", n4)  // wrote 8 bytes
	w.Flush()

	// 追加写入
	f, err = os.OpenFile("/tmp/dat2", os.O_WRONLY|os.O_APPEND, 0666)
	check(err)
	f.WriteString("append\n")
	f.Sync()

}
