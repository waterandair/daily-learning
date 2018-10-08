package main

import (
	b64 "encoding/base64"
	"fmt"
)

// base64 编码

func main() {
	data := "abc123!?$*&()'-=@~"

	// 标准编码
	sEnc := b64.StdEncoding.EncodeToString([]byte(data))
	fmt.Println(sEnc)  // YWJjMTIzIT8kKiYoKSctPUB+

	// 标准解码
	sDec, _ :=  b64.StdEncoding.DecodeString(sEnc)
	fmt.Println(string(sDec))  // abc123!?$*&()'-=@~
	fmt.Println()

	// 适用于 url 的 base64 编码
	uEnc := b64.URLEncoding.EncodeToString([]byte(data))
	fmt.Println(uEnc)  // YWJjMTIzIT8kKiYoKSctPUB-
	uDec, _ := b64.URLEncoding.DecodeString(uEnc)
	fmt.Println(string(uDec))  // abc123!?$*&()'-=@~


}