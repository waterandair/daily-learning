package main

import (
	"fmt"
	"strings"
	"strconv"
)

func main() {
	// strings_operate()
	strconv_operate()
}

func strings_operate() {
	// 判断包含
	fmt.Println(strings.Contains("seafood", "foo"))  // true
	fmt.Println(strings.Contains("seafood", "bar"))  // false
	fmt.Println(strings.Contains("seafood", ""))  // true
	fmt.Println(strings.Contains("", ""))  // true

	// 连接
	s := []string{"foo", "bar", "baz"}
	fmt.Println(strings.Join(s, ", "))

	// 查找位置,不包含返回 -1
	fmt.Println(strings.Index("chiken", "ken"))
	fmt.Println(strings.Index("chiken", "drm"))

	// 重复
	fmt.Println("ba" + strings.Repeat("na", 2))

	// 替换
	fmt.Println(strings.Replace("oink oink oink", "k", "ky", 2))
	fmt.Println(strings.Replace("oink oink oink", "oink", "moo", -1))

	// 分割
	fmt.Printf("%q\n", strings.Split("a,b,c", ","))
	fmt.Printf("%q\n", strings.Split("a man a plan a canal panama", "a "))
	fmt.Printf("%q\n", strings.Split(" xyz ", ""))
	fmt.Printf("%q\n", strings.Split("", "Bernardo O'Higgins"))

	// 掐头去尾
	fmt.Printf("[%q]", strings.Trim(" !!! Achtung !!! ", " !"))  // ["Achtung"]

	// s 字符串的空格符,并且按照空格返回 slice
	fmt.Printf("Fields are: %q", strings.Fields("  foo bar  baz   "))

}

func strconv_operate() {
	// Append 系列函数将整数等转换为字符串后，添加到现有的字节数组中。
	str := make([]byte, 0, 100)
	str = strconv.AppendInt(str, 4567, 10)
	str = strconv.AppendBool(str, false)
	str = strconv.AppendQuote(str, "abcdefg")
	str = strconv.AppendQuoteRune(str, '单')
	fmt.Println(string(str))

	// Format 系列函数把其他类型的转换为字符串
	a := strconv.FormatBool(false)
	b := strconv.FormatFloat(123.23, 'g', 12, 64)
	c := strconv.FormatInt(1234, 10)
	d := strconv.FormatUint(12345, 10)
	e := strconv.Itoa(1023)
	fmt.Println(a, b, c, d, e)

	// Parse 系列函数把字符串转换为其他类型
	a1, err := strconv.ParseBool("false")
	checkError(err)
	b1, err := strconv.ParseFloat("123.23", 64)
	checkError(err)
	c1, err := strconv.ParseInt("1234", 10, 64)
	checkError(err)
	d1, err := strconv.ParseUint("12345", 10, 64)
	checkError(err)
	e1, err := strconv.Atoi("1023")
	checkError(err)
	fmt.Println(a1, b1, c1, d1, e1)

}

func checkError(e error){
	if e != nil{
		fmt.Println(e)
	}
}