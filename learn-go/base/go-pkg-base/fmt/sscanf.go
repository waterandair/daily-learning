package main

import "fmt"

/*
从指定字符串str中按说明的格式读取文本，根据格式字符串顺序将数据存入参数中， 它返回成功解析并存入的参数的数量
*/

func main(){
	str := "13 23 45"
	var a,b,c int
	fmt.Sscanf(str,"%d,%d,%d",&a,&b,&c)
	fmt.Println(a,b,c)  // 13 0 0
	fmt.Sscanf(str,"%d %d %d",&a,&b,&c)
	fmt.Println(a,b,c)  // 13 23 45
}
