### 问题描述
并行度的设置一般用两种方法:
1. spark.default.parallelism
2. text.File() 传入第二个参数,指定partition数量(比较少用)

官方推荐,根据总 cpucore,手动设置 spark.default.parallelism 参赛,指定为 cpucore 总数的 2~3 倍

问题:
如果没有使用 Spark SQL(DataFrame),那么整个 spark application 默认所有 stage 的并行度都是设置的那个参数(除非使用 coalesce 算子缩减过 partition 数量)

spark sql 的 stage 的并行度不能自己设定, spark sql 自己会默认根据 hive 表对应的 hdfs 文件的 block,自动设置 spark sql 查询所在的那个 
stage 的并行度,自己通过 spark.default.parallelism 参数指定的并行度没,只会在灭有 spark sql 的 stage 生效

比如第一个stage, 用了 spark sql 从 hive 表中查询出了一些数据,然后做了一些 transformation 操作,接着做了一个 shuffle 操作(groupByKey)
下一个 stage,在 shuffle 操作之后,做了一些 transformation 操作,hive 表,对应了一个 hdfs 文件, 有 20 个 block ,自己设定的spark.default.parallelism
参数为 100. 
事实上,第一个 stage 的并行度,是不受设置参数控制的,和 block 的数量相同,只有 20 个 task , 第二个 stage,才会根据设置的并行度 100 去执行

这种情况导致第一个 stage 的速度,特别慢,第二个 stage 可以特别快

### 优化  
为了解决 spark sql 无法设置并行度和task数量,可以使用 repratition 算子.

可以将用 spark sql 查询出来的 RDD ,使用 reparitition 算子,去重新分区,此时可以分区成多个 partition,比如从 20 个 partition 分区成 100 个
然后,从 repartititon 以后的 RDD ,并行度和 task 数量没, 就会按照预期的来了,就可以避免跟 spark sql 绑定在一个 stage 中的算子,只能使用少
量的 task 去处理大数据以及复杂的算法逻辑




