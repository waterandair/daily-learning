##### docker 原理简单概况
- 容器是一种被做了`隔离`和`限制`的特殊进程
- Namespace 负责进程上下文的隔离。具体有PID，Mount、UTS、IPC、Network，User等等Namespace
- Cgroups 负责为进程设置资源限制，包括CPU，内存，磁盘，网络带宽等等。它以文件和目录的方式组织在操作系统的/sys/fs/cgroup路径下，可以理解为一个子系统目录加上一组资源限制文件的组合。
- docker 的文件系统使用 `chroot` 命令改变自己的根目录 `/`

注意点： 
- Namespace 隔离机制相比虚拟机并不彻底，首先容器与宿主机共享内核，其次一些资源和对象是不能被Namespace隔离的，比如Time
- cgroups 对资源的限制也不尽完善，比如 `/proc` 文件系统的问题，在容器中运行`top`看到的信息是宿主机的，可以使用 lxcfs 解决
- 容器设计的本身，希望容器和应用能够同生命周期