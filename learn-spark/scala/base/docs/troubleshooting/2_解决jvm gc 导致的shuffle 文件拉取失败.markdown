### 现象
在 spark 作业中出现 : shuffle file not found (非常常见的错误)
有的时候,他会偶尔出现一次,重新提交一次,发现又好了.

### 原因(可能是由于 jvm gc 导致的)
比如,executor 的 jvm 进程,可能内存不够用了,那么这时候可能触发了 gc (minor GC 或 full GC). 一旦发生了 gc 之后,就会导致 executor 内,所
有的工作线程全部停止,比如 BlockManager,基于 netty 的网络通信

下一个 stage 的 executor, 可能还没有停止, task 想去上一个 stage 的 task 所在的 executor 拉取属于自己的数据,结果由于对方正在 GC, 就导致
拉取操作没有响应,就可能会报出,shuffle file not found. 但是,可能下一个 stage 又重新提交了 stage 或 task 以后,再执行就没有问题了.

### 解决
#### spark.shuffle.io.maxRetries 3 
shuffle 文件拉取的时候,如果没有拉取到,允许重试的次数
#### spark.shuffle.io.retryWait 5s
每一次重试拉取文件的时间间隔，默认是　5s

默认情况下,假如第一个 stage 的 executor 正在进行漫长的 full gc, 第二个 stage 的 executor 尝试去拉取文件,结果没有拉取到,默认情况下,会
反复重试拉取 3 词,每次间隔是 5s,最多只会等待 3*5=15s, 如果 15s 内没有拉取到 shuffle file, 就会报出 shuffle file not found

针对这种情况,可以进行预备性的参数调节,增大上述两个参数的值,达到比较大的一个值,尽量保证第二个 stage 一定能够拉取到上一个 stage 的输出文件.避免
报 shuffle file not found.然后可能会重新提交 stage 到 task 去执行,但是这样反而对性能也不好 
