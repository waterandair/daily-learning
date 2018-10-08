package main

import (
	"crypto/md5"
	"crypto/sha1"
	"fmt"
)

// 散列签名
func main() {
	s := "sha1 this string"

	h := sha1.New()

	h.Write([]byte(s))

	bs := h.Sum(nil)

	fmt.Println(s)  // sha1 this string
	fmt.Printf("%x\n", bs)  // [207 35 223 34 7 217 154 116 251 225 105 227 235 160 53 230 51 182 93 148]

	m := md5.New()
	m.Write([]byte(s))
	ms := m.Sum(nil)
	fmt.Printf("%x\n", ms)
}
