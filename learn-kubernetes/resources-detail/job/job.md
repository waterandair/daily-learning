# Job 与 CronJob

## Job
Job 处理离线计算任务, 通过定义 Pod 的并行度(spec.parallelism) 和要完成的总的 Pod 数(spec.completions), 去控制 Pod 的创建和删除,
并根据 Pod 的状态是否是完成决定是否重新创建(restartPolicy=Never)一个新的Pod或重启(restartPolicy=OnFailure)Pod里的容器

### 三种用法

#### 1. 外部管理器+Job模板
把Job的YAML文件定义为一个“模板”，然后用一个外部工具控制这些“模板”来生成Job。这种模式最典型的应用，就是TensorFlow社区的KubeFlow项目。
在这种模式下使用Job对象，completions 和parallelism 这两个字段都应该使用默认值1，而不应该自行设置。而作业 Pod 的并行控制，应该完全交由外部工具来进行管理（比如，KubeFlow）。
#### 2. 拥有固定任务数目的并行Job
只关心最后是否有指定数目（spec.completions）个任务成功退出。至于执行时的并行度是多少，并不关心。
#### 3. 指定并行度（parallelism），但不设置固定的completions的值
这种场景中,由于任务数目的总数不固定，所以每一个Pod必须能够知道，自己什么时候可以退出
### 注意
- restartPolicy在Job对象里只允许被设置为Never和OnFailure；而在Deployment对象里，restartPolicy则只允许被设置为Always。   

## CronJob
CronJob 用来管理定时任务,它管理的实际上是 Job 对象