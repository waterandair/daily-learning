package main

import (
	"regexp"
	"fmt"
	"os"
	"net/http"
	"io/ioutil"
	"strings"
)

func main() {
	/*判断是否匹配
	func Match(pattern string, b []byte) (matched bool, error error)
	func MatchReader(pattern string, r io.RuneReader) (matched bool, error error)
	func MatchString(pattern string, s string) (matched bool, error error)
	*/
	//fmt.Println(IsIP("127.0.0.1"))
	//IsNum()

	/* 通过正则查找替换
	func Compile(expr string) (*Regexp, error)
	func CompilePOSIX(expr string) (*Regexp, error)
	func MustCompile(str string) *Regexp
	func MustCompilePOSIX(str string) *Regexp
	*/
	// Crawler()

	/*
		查找
	*/
	Find()
}

func IsIP(ip string) (b bool) {
	if m, _ := regexp.MatchString("^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$", ip); !m {
		return false
	}
	return true
}

func IsNum() {
	if len(os.Args) == 1 {
		fmt.Println("Usage: regexp[string]")
		os.Exit(1)
	} else if m, _ := regexp.MatchString("^[0-9]+$", os.Args[1]); m {
		fmt.Println("是数字")
	} else {
		fmt.Println("不是数字")
	}
}

func Crawler() {
	resp, err := http.Get("http://www.baidu.com")
	if err != nil {
		fmt.Println("http get error")
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("http read error")
	}
	src := string(body)

	// 将 HTML 标签转化成小写
	src = "<bodY>AA</BODY>"
	re, _ := regexp.Compile("<[\\S]+?>")
	src = re.ReplaceAllStringFunc(src, strings.ToLower)
	fmt.Println(src)

	//去除STYLE
	re, _ = regexp.Compile("\\<style[\\S\\s]+?\\</style\\>")
	src = re.ReplaceAllString(src, "")

	//去除SCRIPT
	re, _ = regexp.Compile("\\<script[\\S\\s]+?\\</script\\>")
	src = re.ReplaceAllString(src, "")

	//去除所有尖括号内的HTML代码，并换成换行符
	re, _ = regexp.Compile("\\<[\\S\\s]+?\\>")
	src = re.ReplaceAllString(src, "\n")

	//去除连续的换行符
	re, _ = regexp.Compile("\\s{2,}")
	src = re.ReplaceAllString(src, "\n")

	fmt.Println(strings.TrimSpace(src))
}

func Find() {
	a := "I am learning Go language"
	re, _ := regexp.Compile("[a-z]{2,4}")

	// 查找符合正则的第一个
	one := re.Find([]byte(a))
	fmt.Println(string(one))  // am

	// 查找符合正则的所有 slice, n 小于 0 表示返回全部符合的字符串,否则返回指定长度
	all := re.FindAll([]byte(a), -1)
	for _, v := range all {
		fmt.Println(string(v))
	}

	// 查找第一个符合条件 index 位置, 开始位置和结束位置
	index := re.FindIndex([]byte(a))
	fmt.Println("findindex:", index)

	// 查找所有符合条件的 index
	allindex := re.FindAllIndex([]byte(a), -1)
	fmt.Println("FindAllIndex", allindex)

	re2, _ := regexp.Compile("am(.*)lang(.*)")
	//查找Submatch,返回数组，第一个元素是匹配的全部元素，第二个元素是第一个()里面的，第三个是第二个()里面的
	//下面的输出第一个元素是"am learning Go language"
	//第二个元素是" learning Go "，注意包含空格的输出
	//第三个元素是"uage"
	submatch := re2.FindSubmatch([]byte(a))
	fmt.Println("FindSubmatch", submatch)
	for _, v := range submatch {
		fmt.Println(string(v))
	}

	//定义和上面的FindIndex一样
	submatchindex := re2.FindSubmatchIndex([]byte(a))
	fmt.Println(submatchindex)

	//FindAllSubmatch,查找所有符合条件的子匹配
	submatchall := re2.FindAllSubmatch([]byte(a), -1)
	fmt.Println(submatchall)

	//FindAllSubmatchIndex,查找所有字匹配的index
	submatchallindex := re2.FindAllSubmatchIndex([]byte(a), -1)
	fmt.Println(submatchallindex)

	src := []byte(`
		call hello alice
		hello bob
		call hello eve
	`)
	pat := regexp.MustCompile(`(?m)(call)\s+(?P<cmd>\w+)\s+(?P<arg>.+)\s*$`)
	res := []byte{}
	for _, s := range pat.FindAllSubmatchIndex(src, -1) {
		res = pat.Expand(res, []byte("$cmd('$arg')\n"), src, s)
	}
	fmt.Println(string(res))



}
