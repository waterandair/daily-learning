spark 在 yarn-client 模式下, application 的注册(executor 的申请)和计算是分开的.

standalone 模式下,这两个操作都是 driver 负责的

ApplicationMaster(ExecutorLauncher)负责 executor 的申请;driver负责 job 和 stage 的划分,以及 task 的创建,分配和调度

### yarn-client 模式下,会产生的问题
由于 driver 是启动在本地机器的,而且 driver 是全权负责所有的任务的调度的,也就是说跟 yarn 集群上运行的多个 executor 进行频繁的通信(中间有task
的启动消息,task 的执行统计消息,task 的运行状态,shuffle 的输出结果)

比如有 executor 100个, stage 10个, task 1000个.
每个 stage 运行的时候,都有 1000 个 task 提交到 executor 上面运行,平均每个 executor 有 10个 task.
问题是,driver 频繁的跟 executor 上运行的 1000 个 task 进行通信, 通信消息特别多

在整个 spark 运行的生命周期内,都会频繁的去进行通信和调度,所有这一切通信和调度都是从本地机器上发出去的,和接收到的.本地机器很可能在 30 分钟内
(spark 作业运行的周期内), 进行频繁大量的网络通信,那么此时,你的本地机器的网络通信负载是非常非常高的,会导致本地机器网卡流量激增

### 解决
本地测试用 yarn-client 模式,生产环境用 yarn-cluster 模式