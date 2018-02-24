### 注意使用正确的持久化方式
```scala
usersRDD.cache()
usersRDD.count()
usersRDD.take()
```
这种方式不仅不会生效,还会报错,报 file not found 的错误

正确的持久化方式:
```scala

usersRDD
usersRDD = usersRDD.cache()
val cacheedUsersRDD = usersRDD.cache()
```
之后再去使用 usersRDD, 或者 cachedUsersRDD. 就可以了

### 持久化的容错问题
持久化,大多数的时候,都是会正常工作的,但是有些时候,也可能会出现意外.比如说,缓存在内存中数据,可能丢失掉了,或者存储在磁盘文件中的数据,被误删了

出现上述情况的时候,如果要对这个 RDD 执行某些操作,可能会发现 RDD 的某些 partition 找不到了

对消失的 partition 重新计算,计算完以后再缓存和使用

有些时候,计算某个 RDD, 可能是极其耗时的,可能 RDD 之前有大量的父 RDD, 那么,如果要重新计算一个 partition, 可能要重新计算之前所有的父 RDD 对应
的 partition.

这种情况下,就可以选择对这个 RDD 进行 checkpoint.以防万一.进行 checkpoint,就是将 RDD 的数据,持久化到一份容错的文件系统上(比如 hdfs)

在对这个 RDD 进行计算的时候,如果发现它的缓存数据不见了,优先就是找一下有没有 checkpoint 数据(到 hdfs 上去找),如果有的话,就使用 checkpoint 
数据, 不至于重新计算

checkpoint 有利有弊,利在于,提高了 spark 作业的可靠性,一旦发生问题,还是很可靠的,不用重新计算大量的 rdd;弊在于,进行 checkpoint 操作的时候,
也就是将 rdd 数据写入 hdfs 中的时候,还是会消耗性能的

所以说, checkpoint 是**用性能换可靠性**

### checkpoint 原理
1. 在代码中,用 sparkContext, 设置一个 checkpoint 目录, 可以是一个容错文件系统的目录,比如 hdfs
2. 在代码中, 对需要进行 checkpoint 的 rdd, 执行 RDD.checkpoint()
3. RDDCheckpointData (spark 内部的 API),接管RDD,会标记为 marked for checkpoint ,准备进行 checkpoint
4. job 运行完之后,会调用一个 finalRDD.doCheckpoint() 方法,会顺着 rdd lineage, 回溯扫描,发现有标记为 checkpoint 的 rdd, 就会进行二次
标记, inProgressCheckpoint,正在接受 checkpoint 操作
5. job 执行完之后,就会启动一个内部的新 job, 去将标记为 inProgressCheckpoint 的 rdd 的数据,都写入 hdfs 文件中 (如果 rdd 之前cache过,
会直接从缓存中获取数据,写入 hdfs 中,如果没有 cache 过,那么就会重新计算一遍这个 rdd, 再 checkpoint)
6. 将checkpoint过的rdd之前的依赖rdd，改成一个CheckpointRDD*，强制改变rdd的lineage。后面如果rdd的cache数据获取失败，直接会通过它的
上游CheckpointRDD，去容错的文件系统，比如hdfs，中，获取checkpoint的数据。

