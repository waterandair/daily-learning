#### ifconfig 和 ip addr
二者都可以查看本机的 IP 及相关信息，返回的内容说明如下：  

##### MAC 地址
形如：`ether:98:5a:eb:8b:ed:7c`
##### 网络设备的状态标识
形如 `<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> `  

- UP 表示网卡处于启动的状态
- BROADCAST 表示网卡有广播地址，可以发送广播包
- MTU 表示最大传输单元，默认 1500 字节，表示二层网络包不能超过 1500 字节， 不含 MAC 头14字节和尾4字节
