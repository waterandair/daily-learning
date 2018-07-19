package main

import (
	"os"
	"io"
)

func main() {

}

// defer 可以理解为会go语言的析构函数
// 如果一条语句不够，可以写成匿名函数的形式
// 多个defer遵循先进后出原则，最后一个先被执行
func CopyFile(dst, src string) (w int64, err error) {
	srcFile, err := os.Open(src)
	if err != nil {
		return
	}
	defer srcFile.Close()
	dstFile, err := os.Create(dst)
	if err != nil {
		return
	}
	defer dstFile.Close()

	defer func() {
		srcFile.Close()
		dstFile.Close()
	}()


	return io.Copy(dstFile, srcFile)
}


/*
go 中没有提供构造函数的功能
对象的创建通常交由一个全局的创建函数来完成,以NewXXX 来命名,表示“构造函数”:
*/

type Rect struct {
	x, y float64
	width, height float64
}

func (r *Rect) Area() float64 {
	return r.width * r.height
}

func NewRect(x, y, width, height float64) *Rect {
	return &Rect{x, y, width, height}
}



