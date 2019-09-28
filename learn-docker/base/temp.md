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



 