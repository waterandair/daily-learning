package main

import (
	"github.com/bitly/go-simplejson"
	"fmt"
	"encoding/json"
)

type Server struct {
	ServerName string
	// 能够被赋值的字段必须是可导出字段(即首字母大写)
	serverIP string
	ServerIP2 string `json:"serverIP2"`
	// 只会解析能找得到的字段，找不到的字段会被忽略
	Another string
}

type Serverslice struct {
	Servers []Server
}


func main() {
	// 解析 json
	//Resolve()
	// 生成 json
	Generate()
}

func Resolve(){
	var s Serverslice
	str := `{"servers":[{"serverName":"Shanghai_VPN","serverIP":"127.0.0.1"},{"serverName":"Beijing_VPN","serverIP":"127.0.0.2"}]}`
	json.Unmarshal([]byte(str), &s)
	fmt.Println(s)

	// 在不知道json的结构的情况下，可以解析到interface{}里面
	var f interface{}
	b := []byte(`{"Name":"Wednesday","Age":6,"Parents":["Gomez","Morticia"]}`)
	err := json.Unmarshal(b, &f)
	if err != nil {
		panic("json 解析失败")
	}
	fmt.Println(f)

	// 使用 samplejson
	js, err := simplejson.NewJson([]byte(`{
		"test": {
			"array": [1, "2", 3],
			"int": 10,
			"float": 5.150,
			"bignum": 9223372036854775807,
			"string": "simplejson",
			"bool": true
		}
	}`))

	arr, _ := js.Get("test").Get("array").Array()
	fmt.Println(arr)
	i, _ := js.Get("test").Get("int").Int()
	fmt.Println(i)
	ms := js.Get("test").Get("string").MustString()
	fmt.Println(ms)
}

func Generate() {
	var s Serverslice
	s.Servers = append(s.Servers, Server{ServerName: "Shanghai_VPN", serverIP: "127.0.0.1"})
	s.Servers = append(s.Servers, Server{ServerName: "Beijing_VPN", serverIP: "127.0.0.2"})

	// 只会生成结构体中 首字母大写 的字段, 如果一定要用首字母小写,需要在 struct tag 定义
	b, err := json.Marshal(s)
	if err != nil {
		fmt.Println("json error: ", err)
	}
	fmt.Println(string(b))
}

