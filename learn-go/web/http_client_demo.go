package main

import (
	"fmt"
	"os"
	"net"
	"io/ioutil"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "usage: %s host:port", os.Args[0])
	}
	service := os.Args[1]
	// 获取一个 tcpAddr
	tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
	checkError2(err)
	// 建立一个TCP连接，并返回一个TCPConn类型的对象
	conn, err :=  net.DialTCP("tcp", nil, tcpAddr)
	checkError2(err)
	// 向服务器发送数据
	_, err = conn.Write([]byte("HEAD / HTTP/1.0\r\n\r\n"))
	checkError2(err)
	result, err := ioutil.ReadAll(conn)
	checkError2(err)
	fmt.Println(string(result))
	os.Exit(0)
}

func checkError2(err error)  {
	if err != nil {
		fmt.Fprintf(os.Stderr, "fatal error: %s", err.Error())
		os.Exit(1)
	}
}