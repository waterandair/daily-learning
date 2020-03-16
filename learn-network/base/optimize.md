## 性能指标
- 带宽：表示链路的最大传输速率，单位通常为 b/s （比特/秒）
- 吞吐量：表示没丢包时的最大数据传输速率，单位通常为 b/s（比特/秒）或者 B/s（字节/秒）。吞吐量受带宽限制，而吞吐量/带宽，也就是该网络的使用率。
- 延时：从网络请求发出后，一直到收到远端响应，所需要的时间延迟。
- PPS(Packet Per Second): 以网络包为单位的传输速率.PPS 通常用来评估网络的转发能力.
- 并发连接数： TCP 连接数量
- 丢包率
- 重传率

### ifconfig/ip 查看整体网络状态
```shell script
$ ifconfig eth0
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
      inet 10.240.0.30 netmask 255.240.0.0 broadcast 10.255.255.255
      inet6 fe80::20d:3aff:fe07:cf2a prefixlen 64 scopeid 0x20<link>
      ether 78:0d:3a:07:cf:3a txqueuelen 1000 (Ethernet)
      RX packets 40809142 bytes 9542369803 (9.5 GB)
      RX errors 0 dropped 0 overruns 0 frame 0
      TX packets 32637401 bytes 4815573306 (4.8 GB)
      TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
```

```shell script
$ ip -s addr show dev eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
  link/ether 78:0d:3a:07:cf:3a brd ff:ff:ff:ff:ff:ff
  inet 10.240.0.30/12 brd 10.255.255.255 scope global eth0
      valid_lft forever preferred_lft forever
  inet6 fe80::20d:3aff:fe07:cf2a/64 scope link
      valid_lft forever preferred_lft forever
  RX: bytes packets errors dropped overrun mcast
   9542432350 40809397 0       0       0       193
  TX: bytes packets errors dropped carrier collsns
   4815625265 32637658 0       0       0       0
```

TX/RX 部分说明：  
- errors：表示发生错误的数据包数，比如校验错误、帧同步错误等；
- dropped 表示丢弃的数据包数，即数据包已经收到了 Ring Buffer，但因为内存不足等原因丢包；
- overruns 表示超限数据包数，即网络 I/O 速度过快，导致 Ring Buffer 中的数据包来不及处理（队列满）而导致的丢包；
- carrier 表示发生 carrier 错误的数据包数，比如双工模式不匹配、物理电缆出现问题等；
- collisions 表示碰撞数据包数。


### netstat/ss 查看套接字、网络栈、网络接口以及路由表
#### 查看接收队列、发送队列、本地地址、远端地址、进程 PID 和进程名称等
```shell script
# -l 表示只显示监听套接字
# -t 表示只显示 TCP 套接字
# -n 表示显示数字地址和端口(而不是名字)
# -p 表示显示进程信息
$ ss -ltnp | head -n 3
State    Recv-Q    Send-Q        Local Address:Port        Peer Address:Port
LISTEN   0         128           127.0.0.53%lo:53               0.0.0.0:*        users:(("systemd-resolve",pid=840,fd=13))
LISTEN   0         128                 0.0.0.0:22               0.0.0.0:*        users:(("sshd",pid=1459,fd=3))
```
- Recv-Q(接收队列)：当socket处于`Established`时，表示表示还没有被应用程序取走的字节数；当socket处于`Listening`时，表示 `syn backlog(半连接队列长度)`的当前值，
- Send-Q(发送队列)：当socket处于`Established`时，表示还没有被远端主机确认的字节数；当socket处于`Listening`时，表示最大的 syn backlog 值。

#### 查看协议栈统计信息

```shell script
$ netstat -s
Tcp:
    3244906 active connection openings  # 主动连接
    23143 passive connection openings   # 被动连接
    115732 failed connection attempts   # 失败重试
    2964 connection resets received
    1 connections established
    13025010 segments received
    17606946 segments sent out
    44438 segments retransmitted
    42 bad segments received
    5315 resets sent
    InCsumErrors: 42

$ ss -s
Total: 186 (kernel 1446)
TCP:   4 (estab 1, closed 0, orphaned 0, synrecv 0, timewait 0/0), ports 0

Transport Total     IP        IPv6
*	  1446      -         -
RAW	  2         1         1
UDP	  2         2         0
TCP	  4         3         1
```
#### sar 网络吞吐和 PPS
```shell script
# 每隔1秒输出一组数据
$ sar -n DEV 1
Linux 4.15.0-1035-azure (ubuntu) 	01/06/19 	_x86_64_	(2 CPU)

13:21:40        IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
13:21:41         eth0     18.00     20.00      5.79      4.25      0.00      0.00      0.00      0.00
13:21:41      docker0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
13:21:41           lo      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
```
- rxpck/s 和 txpck/s 分别是接收和发送的 PPS，单位为包/秒。
- rxkB/s 和 txkB/s 分别是接收和发送的吞吐量，单位是KB/秒。
- rxcmp/s 和 txcmp/s 分别是接收和发送的压缩数据包数，单位是包/秒。
- %ifutil 是网络接口的使用率，即半双工模式下为 (rxkB/s+txkB/s)/Bandwidth，而全双工模式下为 max(rxkB/s, txkB/s)/Bandwidth。

`Bandwidth` 可以用 `ethtool` 来查询，它的单位通常是 Gb/s 或者 Mb/s。
```shell script
$ ethtool eth0 | grep Speed
	Speed: 1000Mb/s
```