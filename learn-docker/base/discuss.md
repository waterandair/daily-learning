##### docker 原理简单概况
容器:  
- 容器是一种被做了`隔离`和`限制`的特殊进程
- Namespace 负责进程上下文的隔离。具体有PID，Mount、UTS、IPC、Network，User等等Namespace
- Cgroups 负责为进程设置资源限制，包括CPU，内存，磁盘，网络带宽等等。它以文件和目录的方式组织在操作系统的/sys/fs/cgroup路径下，可以理解为一个子系统目录加上一组资源限制文件的组合。

容器镜像:  
- docker 的文件系统使用 `chroot` 命令改变自己的根目录 `/`,为了能够让容器的这个根目录看起来更“真实”,一般会在这个容器的根目录下挂载一个完整操作系统的文件系统,比如 Ubuntu16.04 的 ISO。这就是容器镜像
- 容器镜像也可以叫作 `rootfs`(根文件系统), 是挂载在容器根目录上,用来为容器进程提供隔离后执行环境的文件系统.
- docker 镜像引入了 `layer`(层)概念,镜像由许多 layer 通过 Union File System(联合文件系统) 挂载到同一个目录下,形成一个完整的镜像
- Dockerfile中的每个原语执行后，都会生成一个对应的镜像层
- docker 的 layer 可以分为三部分,以一个使用 ubuntu 系统的镜像,由下到上有7层,分别为:
- - 只读层(ro+wh)(5层): 对应的是 ubuntu:latest 镜像的5层,即一个完整的ubuntu系统文件系统, wh 表示 whiteout,是联合文件系统删除一个文件的方式,后面详细说明 
- - Init 层(ro+wh)(1层): 一个单独的内部层,专门用来存放 /etc/hosts,/etc/resolv.conf 等文件,对这些文件的修改仅在当前容器有效,不会被 docker commit 提交
- - 可读写层(rw)(1层): 在容器中所有的增删改都会以增量的方式出现在可读写层,这些修改会随着 docker commit 提交到镜像中

删除只读层的文件,理解 whiteout:  
如果用户希望删除只读层里的文件,Union File System(常用AuFS)会在可读写层创建一个 whiteout 文件, 把只读层里的文件"遮挡"起来, 比如
删除只读层里的 foo 文件,实际上是创建了一个名为 .wh.foo 的文件,当这两个层被联合挂载后, foo 文件会被 .wh.foo 文件遮挡起来,对于用户来说,就好像它被删除了.  

修改只读层的文件,理解 copy-on-white:  
修改操作只能作用到可读写层,但对于相同的文件,可读写层会覆盖只读层,所有当在可读写层修改一个文件的时候,首先会在只读层查到有没有相同的文件,
如果有,就将其复制到可读写层,然后在可读写层想修改,对于用来来说,就可以看到该文件被进行了修改.这种方式被称为 copy-on-white.

注意点： 
- Namespace 隔离机制相比虚拟机并不彻底，首先容器与宿主机共享内核，其次一些资源和对象是不能被Namespace隔离的，比如Time
- cgroups 对资源的限制也不尽完善，比如 `/proc` 文件系统的问题，在容器中运行`top`看到的信息是宿主机的，可以使用 lxcfs 解决
- 容器设计的本身，希望容器和应用能够同生命周期
##### exec模式 和 shell 模式
###### exec 模式(推荐)
- exec 模式执行的命令在容器中的 pid 为 1 (这一点很重要)
- exec 模式不会通过shell执行相关命令
- 注意 exec 模式中每个命令都要用双引号
示例: 
```dockerfile
FROM ubuntu
CMD ["top"]
```
用上面的 Dockerfile 构建一个容器并进入容器, 可以查到到 `top` 的pid 为1
```dockerfile
FROM ubuntu
CMD ["echo", "$HOME"]
``` 
因为 exec 模式不会通过shell执行,所有用上面的 dockerfile 构建的容器无法取出环境变量 $HOME
可以将 dockerfile 做如下修改:
```dockerfile
FROM ubuntu
CMD ["sh", "-c", "echo $HOME"]
```

###### shell 模式
- shell 会以 `/bin/sh -c "command"` 执行命令,所以容器中 pid 为 1 的进程是 bash 进程,而不是任务进程

##### 区别 Dockerfile 中 CMD 和 ENTRYPOINT 指令
- docker 提供这两个作用相似的命令,是为了处理容器启动时,命令行参数的行为.
- CMD 和 ENTRYPOINT 都支持 exec 模式和 shell 模式
- 通过 CMD 执行的命令, 会被执行`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]` 时指定的`[COMMAND] [ARG...]`替换掉.
- 通过 ENTRYPOINT exec模式执行的命令, 会追加 `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]` 时指定的`[COMMAND] [ARG...]`
- 通过 ENTRYPOINT shell 模式执行的命令时,会完全忽略 `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]` 时指定的`[COMMAND] [ARG...]`
- ENTRYPOINT 的指令也可以被覆盖, 需要显示指定参数 `docker run --entrypoint [COMMAND]`
- 同时使用 CMD 和 ENTRYPOINT 时,常常把 CMD 指定的内容当做默认值   

同时使用 CMD 和 ENTRYPOINT 的情况比较复杂,官方给出了一个[表格](https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact)帮助理解,翻译如下:  
CMD 和 ENTRYPOINT 都用于说明在容器运行时执行的命令,要遵循下面的几条规则:
- Dockerfile 中只要指定 CMD 和 ENTRYPOINT 中的一个
- 当容器被当做一个可执行程序的时候,应该定义 ENTRYPOINT
- CMD 应该被用于为 ENTRYPOINT 命令指定默认参数,或执行临时命令
- CMD 被被启动容器时指定的额外参数覆盖  
下面的表格展示了 CMD 和 ENTRYPOINT 在执行命令时的行为:

 _| 没有 ENTRYPOINT | ENTRYPOINT exec_entry p1_entry | ENTYRPOINT ["exec_entry", "p1_entry"] 
---|--- | --- | --- | 
没有 CMD | 启动报错 | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry 
CMD [“exec_cmd”, “p1_cmd”] | exec_cmd p1_cmd	| /bin/sh -c exec_entry p1_entry | exec_entry p1_entry exec_cmd p1_cmd
CMD [“p1_cmd”, “p2_cmd”] |	p1_cmd p2_cmd |	/bin/sh -c exec_entry p1_entry | exec_entry p1_entry p1_cmd p2_cmd
CMD exec_cmd p1_cmd | /bin/sh -c exec_cmd p1_cmd | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry /bin/sh -c exec_cmd p1_cmd

##### 理解 `docker exec` 命令的原理  
- 一个容器的 Namespace 信息可以在宿主机看到,它们在 `/proc/容器pid/ns` 目录下.
- 利用系统调用 `setns` 将当前进程加入到某个 Namespace 中

##### 注意镜像的分层概念
`Note that each instruction is run independently, and causes a new image to be created - so RUN cd /tmp will not have any effect on the next instructions.`  

每个指令都是独立运行的，都会构建一个新的镜像，所以不能用写 shell 的习惯写 Dockerfile， 比如在 Dockerfile 中写入执行 `RUN cd /tmp`， 并不会对后面的指令产生影响。    
##### docker build -f /path/dir
build 指令并不是由命令行程序完成的，而是转发给 `docker daemon` 完成的，因为执行此命令，会递归的将 `/path/dir`所有的文件和文件夹发送给 `docker daemon`

##### 来自 dockerfile_best-practices 的注意点
- 使用 alpine 作为基础镜像
- `apt-get update` 和 `apt-get install -y` 要在一个 RUN 中运行， 在运行完后，要执行 
- 使用`pipe`要注意，docker 只会判断 `pipe` 中的最后一个命令，即使前面的命令有错误，也会构建成功。如果要避免这种情况，可以在指令最前面加 `set -o pipefail`
- `ADD`和`COPY`作用很像，但`COPY`的含义更清晰，永远建议使用`COPY`。如有多个文件需要`COPY`,仅在需要用到的时候分别`COPY`
- `WORKDIR` 永远是绝对路径
- `EXPOSE` 仅仅是声明，方便使用者理解，或者是在 `docker run -P`的时候不需要默认指定 `EXPOSE`的端口。
- `VOLUME` 定义匿名卷，确保应用不会再容器内写入数据，在启动容器时，可以为它们指定 volume
