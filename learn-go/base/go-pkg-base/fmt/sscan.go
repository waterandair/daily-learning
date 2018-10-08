package main

import "fmt"

/*
这个函数主要是从指定源字符串str中读取文本，将空白分割的连续数据顺序存入参数里。
换行视同空白。它返回成功读取的参数的数量。
如果少于提供的参数的数量，返回值err将报告原因。
*/

func main(){
	str := "34  343  245"
	var a,b,c int
	fmt.Sscan(str,&a,&b,&c)
	fmt.Println(a,b,c)  // 34 343 245

	var x, y, z string

	fmt.Sscan("aaaaaaaaaaaaaaa as asd ", &x, &y, &z)
	fmt.Println(x, y, z, "b")
}
