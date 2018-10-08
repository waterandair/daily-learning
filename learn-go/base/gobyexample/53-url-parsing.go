package main

import (
	"fmt"
	"net"
	"net/url"
)

// 解析 url

func main() {
	s := "postgres://user:pass@host.com:5432/path?k=v&k1=k2#f"

	u, err := url.Parse(s)
	if err != nil {
		panic(err)
	}

	fmt.Println(u.Scheme)  // postgres
	fmt.Println(u.User)  // user:pass
	fmt.Println(u.User.Username())  // user
	p, _ := u.User.Password()
	fmt.Println(p)  // pass

	fmt.Println(u.Host)  // host.com:5432
	host, port, _ := net.SplitHostPort(u.Host)
	fmt.Println(host, port)  // host.com 5432

	fmt.Println(u.Path)  // /path
	fmt.Println(u.Fragment)  // f

	fmt.Println(u.RawQuery)  // k=v&k1=k2
	m, _ := url.ParseQuery(u.RawQuery)
	fmt.Println(m)  // map[k:[v] k1:[k2]]
	fmt.Println(m["k"][0])  // v
}

