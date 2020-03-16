#### sar
查看系统的网络收发情况，不仅可以观察网络收发的吞吐量（BPS，每秒收发的字节数），还可以观察网络收发的 PPS(每秒收发的网络帧数)

- -n DEV 显示网络收发的报告，间隔 1s 输出一组数据 
```shell script
$ sar -n DEV 1
root@ubuntu-vm:~# sar -n DEV 1
Linux 4.15.0-88-generic (ubuntu-vm) 	03/13/20 	_x86_64_	(1 CPU)

20:23:40        IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
20:23:41           lo      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
20:23:41       enp0s2      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
```

从左往右依次是：  

- 报告的时间
- IFACE 表示网卡
- rxpck/s 和 txpck/s 分别表示每秒接收、发送的网络帧数，也就是 PPS
- rxkB/s 和 txkB/s 分别表示每秒接收、发送的千字节数，也就是 BPS

接收网络帧的平均大小 = （rxkB/s）* 1024 / (rxpck/s)  

#### tcpdump
