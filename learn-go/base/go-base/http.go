package main

import (
	"net/http"
	"io"
	"os"
	"net/url"
	"fmt"
	"io/ioutil"
	"strings"
)

func main() {
	// get()
	// post()
	// post_form()
	// head()
	do()
}

// http.Get()
func get() {
	resp, err := http.Get("http://127.0.0.1:8000")
	if err != nil {
		// 错误处理
		return
	}
	defer resp.Body.Close()
	io.Copy(os.Stdout, resp.Body)
}

func post() {
	resp, err := http.Post(
		"http://127.0.0.1:8000/login",
		"application/x-www-form-urlencoded",
		strings.NewReader("username=zj"))
	if err != nil {
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)

	fmt.Println(string(body))
}

// http.PostForm()
func post_form() {
	resp, err := http.PostForm("http://127.0.0.1:8000/login", url.Values{
		"username": {"zj"},
		"password": {"000000"},

	})
	if err != nil {
		// 处理错误
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)

	fmt.Println(string(body))
}

// http.Head()  请求头信息
func head()  {
	res, err := http.Head("http://127.0.0.1:8000")
	if err != nil {
		return
	}
	fmt.Println(res.Header["Content-Type"])
}

// (*http.Client).Do()  用于需要定制 http 请求头的场景
func do() {
	req, err := http.NewRequest("GET", "http://127.0.0.1:8000", nil)
	if err != nil {
		fmt.Println(err)
	}

	req.Header.Add("User-Agent", "test")
	client := &http.Client{

	}
	res, err := client.Do(req)
	fmt.Println(res.Header["User-Agent"])
}