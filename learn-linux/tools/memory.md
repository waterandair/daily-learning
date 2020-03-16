#### free 查看系统内存情况
```shell script
root@ubuntu-vm:~# free
              total        used        free      shared  buff/cache   available
Mem:        4040012       90652     3365836         560      583524     3709736
Swap:             0           0           0
```

- total: 总大小 
- used: 已使用内存大小，包含共享内存
- free: 未使用的内存大小
- shared: 共享内存大小
- buff/cache: 缓冲区和缓存大小
- available：新进程可用的大小(包含未使用的内存和缓存的内存)

#### top/ps 查看进程的内存使用情况

```shell script
top - 09:00:02 up 20:23,  2 users,  load average: 0.00, 0.00, 0.00
Tasks: 102 total,   1 running,  55 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  4040012 total,  3365020 free,    91408 used,   583584 buff/cache
KiB Swap:        0 total,        0 free,        0 used.  3708972 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
 2013 root      20   0  107984   7096   6092 S  0.3  0.2   0:21.20 sshd                                                1 root      20   0   78004   9104   6680 S  0.0  0.2   0:02.68 systemd
``` 
- VIRT 虚拟内存，只要是进程申请过的内存，即便还没有真正分配物理内存，也会计算在内。
- RES 是常驻内存的大小，也就是进程实际使用的物理内存大小，但不包括 Swap 和共享内存。
- SHR 是共享内存的大小，比如与其他进程共同使用的共享内存、加载的动态链接库以及程序的代码段等。
- %MEM 是进程使用物理内存占系统总内存的百分比 
