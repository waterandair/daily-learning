package main

import (
	"net"
	"time"
	"strings"
	"strconv"
	"fmt"
)

func main() {

	service := ":7777"
	tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
	checkError2(err)
	listener, err := net.ListenTCP("tcp", tcpAddr)
	checkError2(err)

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}

		go handleClient(conn)
	}
}

func handleClient(conn net.Conn) {
	conn.SetReadDeadline(time.Now().Add(2 * time.Minute))
	request := make([]byte, 128) // set maxium request length to 128B to prevent flood attack
	defer conn.Close()

	for {
		read_len, err := conn.Read(request)

		if err != nil {
			fmt.Println(err)
			break
		}

		if read_len == 0 {
			break // connection already closed by client
		} else if strings.TrimSpace(string(request[:read_len])) == "timestamp" {
			daytime := strconv.FormatInt(time.Now().Unix(), 10)
			conn.Write([]byte(daytime))
		} else {
			daytime := time.Now().String()
			conn.Write([]byte(daytime))
		}

		request = make([]byte, 128) // clear last read content
	}
}
