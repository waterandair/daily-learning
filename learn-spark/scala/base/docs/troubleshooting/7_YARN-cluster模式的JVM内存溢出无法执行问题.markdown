### yarn-client 和 yarn-cluster 模式的不同之处

yarn-client 模式,driver 运行在本地机器上;
yarn-cluster 模式,driver 运行在 yarn集群上某个 nodemanager 节点上面

yarn-client 本地机器负责 spark 作业的调度,所以网卡流量会激增,yarn-cluster 就没有这个问题

yarn-client 的 driver 运行在本地,通常来说本地机器跟 yarn 集群都不会在一个机房,所以性能可能不是特别好;
yarn-cluster 模式下,driver 是跟 yarn 集群运行在一个机房内,性能上来说,也会好一点

### yarn-cluster 可能会出现的问题
有的时候,运行一些包含 spark-sql 的 spark 作业,可能会碰到 yarn-client 模式下,可以正常提交运行;yarn-cluster 模式下,可能是无法提交运行的,
会报出 JVM 的 PermGen(永久代) 的内存溢出, OOM

yarn-client 模式下,driver 是运行再本地机器上的,spark 使用的 JVM 的 PermGen 的配置,是本地 spark-class 文件(spark 客户端是默认有配置的),
JVM 的永久代的大小是 128M, 这个是没有问题的;但是, yarn-cluster 模式下,driver 是运行再 yarn 集群的某个节点上的,使用的是没有经过配置的默认设置
(82M).

对于 spark-sql, 它的内部是要进行很复杂的 sql 语义解析,语法树的转换等操作,在这种复杂的情况下,如果 sql 本身特别复杂的话,很可能会导致性能的消耗,
内存的消耗,可能会 PermGen 永久代的占用会特别大.

所以,如果对永久代的占用需求,超过了 82M 的话,但是又在 128M 以内,就会出现 PermGen Out of Memory error log 的错误.

### 解决
设置 driver 永久代的大小,默认是 128M, 最大是 256M.那么,这样的话,就可以基本保证spark作业不会出现上述的 yarn-cluster 模式导致的永久代内存
溢出的问题
```shell
--conf spark.driver.extraJavaOptions="-XX:PermSize=128M -XX:MaxPermSize=256M"
```

### 使用spark-sql要注意
当有大量"or"语句时,可能会出现 driver 端的jvm stack overflow，JVM栈内存溢出的问题

JVM栈内存溢出，基本上就是由于调用的方法层级过多，因为产生了大量的，非常深的，超出了JVM栈深度限制的，递归。递归方法。spark sql，有大量or语句
的时候，spark sql内部源码中，在解析sql，比如转换成语法树，或者进行执行计划的生成的时候，对or的处理是递归。or特别多的话，就会发生大量的递归。

可以把用 or 过多的语句转换成多条语句

每条 sql 语句100个 or 子句 以内,通常不会出现问题


