package main

import (
	"fmt"
	"strconv"
)

func main() {
	f, _ := strconv.ParseFloat("1.234", 64)
	fmt.Println(f)  // 1.234

	i, _ := strconv.ParseInt("123", 0, 64)
	fmt.Println(i)  // 123

	// 十六进制
	d, _ := strconv.ParseInt("0x1c8", 0, 64)
	fmt.Println(d)  // 456

	u, _ := strconv.ParseUint("-789", 0, 64)
	fmt.Println(u)  // 0

	k, _ := strconv.Atoi("135")
	fmt.Println(k)  // 135

	_, e := strconv.Atoi("wat")
	fmt.Println(e)  // strconv.Atoi: parsing "wat": invalid syntax
}
