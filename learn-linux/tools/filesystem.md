#### df 查看文件系统的磁盘空间
```shell script
root@ubuntu-vm:~# df -h /dev/sda1
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        39G  1.2G   38G   4% /
```
```shell script
# 查看索引节点的占用空间
# 如果发现索引节点不足，但磁盘空间充足，就说明是过多的小文件引起的
root@ubuntu-vm:~# df -i -h /dev/sda1
Filesystem     Inodes IUsed IFree IUse% Mounted on
/dev/sda1        5.0M   69K  4.9M    2% /

```

#### iostat 磁盘IO整体性能观测
```shell script
root@ubuntu-vm:~# iostat -d -x 1
Linux 4.15.0-88-generic (ubuntu-vm) 	03/16/20 	_x86_64_	(1 CPU)

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
loop0            0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     1.60     0.00   0.00   0.00
sda              0.20    0.33      2.56     19.11     0.01     0.17   3.86  34.22    1.09    7.13   0.00    12.74    58.66   0.72   0.04
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.15    0.00   0.00     3.73     0.00   0.15   0.00
```
- 使用率: %util
- IOPS: r/s + w/s
- 吞吐量： rKB/s + wKB/s
- 响应时间： r_await + w_await

#### pidstat / iotop 进程IO观测
```shell script
root@ubuntu-vm:~# pidstat -d 1
Linux 4.15.0-88-generic (ubuntu-vm) 	03/16/20 	_x86_64_	(1 CPU)

09:53:46      UID       PID   kB_rd/s   kB_wr/s kB_ccwr/s iodelay  Command

09:53:47      UID       PID   kB_rd/s   kB_wr/s kB_ccwr/s iodelay  Command
```  
    