package main

/* go 对 socket 的操作都用 Dial 函数简化
	conn, err := net.Dial("tcp", "192.168.0.10:2100")  // tcp 连接
	conn, err := net.Dial("udp", "192.168.0.12:975")  // udp 连接
	conn, err := net.Dial("ip4:icmp", "www.baidu.com")  // icmp 连接

Dial() 函数支持如下几种网络协议: "tcp" 、 "tcp4" (仅限IPv4)、 "tcp6" (仅限
IPv6)、 "udp" 、 "udp4" (仅限IPv4)、 "udp6" (仅限IPv6)、 "ip" 、 "ip4" (仅限IPv4)和 "ip6"
(仅限IPv6)。

发送数据时,使用 conn 的 Write()成员方法,接收数据时使用 Read() 方法。


net 包中还包含了一系列的工具函数
	验证IP地址有效性：
		net.ParseIP()
	创建子网掩码：
		func IPv4Mask(a, b, c, d byte) IPMask
	获取默认子网掩码：
		func (ip IP) DefaultMask() IPMask
	根据域名查找IP：
		func ResolveIPAddr(net, addr string) (*IPAddr, error)
		func LookupHost(name string) (cname string, addrs []string, err error);
*/

func main() {

}

