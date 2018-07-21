package main

import (
	"net/http"
	"strings"
	"fmt"
	"log"
	"html/template"
	"time"
	"crypto/md5"
	"io"
	"strconv"
	"os"
)

func main() {
	http.HandleFunc("/", sayHelloName)  // 设置路由
	http.HandleFunc("/login", login)
	http.HandleFunc("/upload", upload)

	err := http.ListenAndServe(":8000", nil)  // 设置监听的端口
	if err != nil {
		log.Fatal("ListenAndServe:", err)
	}
}

func sayHelloName(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()  // 解析参数, 默认不解析
	fmt.Println(r.Form)
	fmt.Println("path", r.URL.Path)
	fmt.Println("scheme", r.URL.Scheme)
	fmt.Println(r.Form["url_long"])
	for k, v := range r.Form {
		print("key: ", k, " ")
		fmt.Println("value: ", strings.Join(v, " "))
	}
	userAgent := r.Header["User-Agent"]
	w.Header()["User-Agent"] = userAgent
	fmt.Fprint(w, "hello world")  // 这个写入到 w 的是输出到客户端的
}

func login(w http.ResponseWriter, r *http.Request) {
	fmt.Println("method", r.Method)
	if r.Method == "GET" {
		//t, _ := template.ParseFiles("login.html")
		//log.Println(t.Execute(w, nil))
	} else {
		r.ParseForm()
		// 请求的是登录,执行登录逻辑
		fmt.Println("username: ", template.HTMLEscapeString(r.Form.Get("username")))
		fmt.Println("password: ", template.HTMLEscapeString(r.Form.Get("password")))
		fmt.Fprint(w, "username:", r.Form.Get("username"))
		//fmt.Fprint(w, "password:", r.Form.Get("password"))
		// 转义后输出到客户端
		// template.HTMLEscape(w, []byte(r.Form.Get("username")))
	}
}

func upload(w http.ResponseWriter, r *http.Request) {
	fmt.Println("method:", r.Method)  // 获取请求的方法
	if r.Method == "GET" {
		crutime := time.Now().Unix()
		h := md5.New()
		io.WriteString(h, strconv.FormatInt(crutime, 10))
		token := fmt.Sprintf("%x", h.Sum(nil))

		t, _ := template.ParseFiles("upload.html")
		t.Execute(w, token)
	} else {
		r.ParseMultipartForm(32 << 20)
		file, handler, err := r.FormFile("uploadfile")
		if err != nil {
			fmt.Println(err)
			return
		}

		defer file.Close()
		fmt.Fprintf(w, "%v", handler.Header)
		f, err := os.OpenFile("./test/" + handler.Filename, os.O_WRONLY|os.O_CREATE, 0666)
		if err != nil {
			fmt.Println(err)
			return
		}
		defer f.Close()
		io.Copy(f, file)
	}
}

