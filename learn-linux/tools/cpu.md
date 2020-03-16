#### vmstat

#### mpstat 查看整体 cpu 负载 
```shell script
# 监控所有CPU， 5 秒输出一次数据
mpstat -P ALL 5 1
# 监控 0 号CPU， 5 秒输出一次数据
mpstat -P 0 5 1
```

#### 查看 CPU 上下文切换
```shell script
# 内存和CPU监控工具
vmstat 5 
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 209472 907632 1374700    0    0   151   163    0    1  2  1 97  0  0
 0  0      0 216068 907648 1374756    0    0     0    49 2879 5446  1  1 97  0  0
 0  0      0 216040 907656 1374784    0    0     0    40 2127 3699  1  1 98  0  0
 2  0      0 214216 907660 1374824    0    0     0    68 2180 3793  1  1 98  0  0
```
- r (Running or Runnable）：就绪队列的长度，也就是正在运行和等待CPU的进程数， 大于CPU数表示当前存在大量CPU竞争
- b（Blocked）：处于不可中断睡眠状态的进程数 
- cs（context switch）：每秒上下文切换的次数。 
- in（interrupt）：是每秒中断的次数。

#### pidstat 进程性能分析工具
-w 进程上下文切换
-u CPU使用率
-t 显示线程数据，默认显示进程数据
-d I/O 统计数据
-p 指定进程号

```shell script
# 间隔 1s 输出 10 组数据
$pidstat -w -u 1 10

14:36:23      UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command

14:36:23      UID       PID   cswch/s nvcswch/s  Command
14:36:24        0         7      1.98      0.00  ksoftirqd/0
14:36:24        0         8      2.97      0.00  rcu_sched
14:36:24        0      1896      0.99      0.00  kworker/0:0
14:36:24        0     19592      0.99      0.00  pidstat

14:36:24      UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command

14:36:24      UID       PID   cswch/s nvcswch/s  Command
14:36:25        0         7      1.92      0.00  ksoftirqd/0
14:36:25        0         8      2.88      0.00  rcu_sched
14:36:25        0      1896      0.96      0.00  kworker/0:0
14:36:25        0      2013     11.54      0.96  sshd
14:36:25        0     18327     39.42      0.00  kworker/u2:2
14:36:25        0     19592      0.96     39.42  pidstat
```
- cswch(voluntary context switches)： 每秒自愿上下文切换, 进程无法获取所需资源，比如I/O、内存等系统资源不足。
- nvcswch(non voluntary context switches)： 每秒非自愿上下文切换，进程由于时间片已到等原因，被系统强制调度，比如大量进程都在争抢 CPU 时

#### cat /proc/interrupts 观察 CPU 中断
```shell script
watch -d cat /proc/interrupts
```

#### dstat 结合了vmstat、iostat、ifstat，观察 CPU、磁盘 I/O、网络以及内存
```shell script
# 每秒一次 输出10组数据
root@ubuntu-vm:~# dstat 1 10
You did not select any stats, using -cdngy by default.
--total-cpu-usage-- -dsk/total- -net/total- ---paging-- ---system--
usr sys idl wai stl| read  writ| recv  send|  in   out | int   csw
  1   0  99   0   0|6856B   47k|   0     0 |   0     0 |  15    41
  0   0 100   0   0|   0    44k| 330B  974B|   0     0 |  22    59
  0   0 100   0   0|   0     0 | 132B  428B|   0     0 |   6    13
  0   0 100   0   0|   0     0 | 132B  444B|   0     0 |   7     9
  0   0 100   0   0|   0     0 | 132B  436B|   0     0 |   7    11
  0   0 100   0   0|   0     0 | 132B  436B|   0     0 |   6    14
  0   0 100   0   0|   0     0 | 132B  436B|   0     0 |   8    13
  0   0 100   0   0|   0     0 | 132B  436B|   0     0 |   7    12
  0   0 100   0   0|   0     0 | 132B  436B|   0     0 |   7    13
  0   0 100   0   0|   0     0 | 132B  436B|   0     0 |   7     9
```

#### top 查看总体的 CPU 和内存，以及各进程的资源使用情况

```
top - 16:02:36 up 10:35,  3 users,  load average: 0.00, 0.00, 0.00
Tasks: 104 total,   1 running,  57 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  4040012 total,  3407860 free,    93480 used,   538672 buff/cache
KiB Swap:        0 total,        0 free,        0 used.  3709332 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
 2013 root      20   0  107984   7096   6092 S  0.3  0.2   0:19.89 sshd
    1 root      20   0   77932   9048   6680 S  0.0  0.2   0:02.09 systemd
    2 root      20   0       0      0      0 S  0.0  0.0   0:00.00 kthreadd
    4 root       0 -20       0      0      0 I  0.0  0.0   0:00.00 kworker/0:
```
##### CPU 相关指标
- us(user): 用户态 CPU 时间。不包括 nice 时间，但包括了 guest 时间
- ni(nice): 低优先级用户态 CPU 时间，也就是进程的 nice 值被调整为 1-19 之间时的 CPU 时间。nice 可取值范围是 -20 到 19，数值越大，优先级越低
- sys(system): 内核态 CPU 时间
- id(idle): 代表空闲时间。不包括等待 I/O 的时间（iowait）
- wa(iowait): 代表等待 I/O 的 CPU 时间
- hi(irq): 代表处理硬中断的 CPU 时间
- si(softirq): 代表处理软中断的 CPU 时间
- st(steal): 代表当系统运行在虚拟机中的时候，被其他虚拟机占用的 CPU 时间
- guest: 代表通过虚拟化运行其他操作系统的时间，也就是运行虚拟机的 CPU 时间
- gnice(guest_nice): 代表以低优先级运行虚拟机的时间
##### 进程相关指标
###### 状态
- R(Running)：进程在 CPU 的就绪队列中，正在运行或者正在等待运行
- D(Disk Sleep): 不可中断状态睡眠（Uninterruptible Sleep,一般表示进程正在跟硬件交互，并且交互过程不允许被其他进程或中断打断。
- Z(Zombie): 僵尸进程，实际上已经结束了，但父进程没有调用 wait(),waitpid() 回收子进程资源（比如进程的描述符、PID 等），也没有处理子进程在结束时发出的 SIGCHLD 信号。子进程执行过快也会导致这个问题。最坏的结果是用尽 pid，导致无法开启新的进程
- S(Interruptible Sleep): 可中断状态睡眠,表示进程因为等待某个事件而被系统挂起。当进程等待的事件发生时，它会被唤醒并进入 R 状态。
- I(Idle): 空闲状态，用在不可中断睡眠的内核线程上。硬件交互导致的不可中断进程用 D 表示，但对某些内核线程来说，它们有可能实际上并没有任何负载，用 Idle 正是为了区分这种情况。要注意，D 状态的进程会导致平均负载升高，I 状态的进程却不会。
- T(Traced): 进程处于暂停或者跟踪状态，比如向一个进程发送 SIGSTOP 信号，或者使用调试器调试代码时设置的断点，都会使进程变成此状态
- X(Dead): 进程已经消亡

#### strace 追踪进程的系统调用
```shell script
# 查看 pid 为 6082 的进程的系统调用
# -f 显示线程追踪
strace -p 6082
```