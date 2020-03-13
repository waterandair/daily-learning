#### stress


#### sysbench
sysbench 是一个基于 luaJIT 开发的多线程基准开发工具，常用于评估数据库负载，亦可模拟上下文切换过多的场景。

```shell script
# 以10个线程运行5分钟的基准测试，模拟多线程切换的问题
sysbench --threads=10 --max-time=300 threads run

# 
```