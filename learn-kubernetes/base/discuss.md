## 笔记&讨论

### 核心组件简介

组件 | 作用
---|---
etcd | 保存了整个集群的状态
kube-apiserver | 提供了资源操作的唯一入口,并提供认证、授权、访问控制、API注册和发现等机制
kube-controller-manager | 负责维护集群的状态,比如故障检测、自动扩展、滚动更新等  
kube-scheduler | 负责资源的调度,按照预定的调度策略将 Pod 调度到相应的机器上  
kubelet | 负责维持容器的生命周期,同时也负责 Volume(CVI)和网络(CNI)的管理  
Container runtime | 负责镜像管理以及 Pod 和容器的真正运行(CRI),默认的容器运行时为 Docker  
kube-proxy | 负责为 Service 提供 cluster 内部的服务发现和负载均衡  

### 核心技术概念和API对象
对象 | 作用简介
---|---  
Pod | 最小单元;多容器组合完成任务,共享网络栈和文件系统
RC (Replication Controller) | 最早保证高可用的API对象.
RS (Replication Set) | 新一代的 RC, 支持更多种类的匹配,一般不单独使用,而是作为 Deployment 的理想状态参数使用  
Deployment | 未来对所有长期伺服型的的业务的管理,都会通过Deployment来管理. 它可以用来创建一个新的服务,更新一个新的服务,也可以是滚动升级一个服务,它通过ReplicaSet的个数来描述应用的版本；然后，它再通过ReplicaSet的属性（比如replicas的值），来保证Pod的副本数量。Deployment 只允许容器 restartPolicy=Always,
Service | 通过虚拟IP + 服务发现 + 负载均衡,解决访问 Pod 的问题,负载均衡由 kube-proxy 实现.  
Job | 批处理型任务的API对象,此类型的 Pod,在任务完成后就自动退出.  
DaemonSet | 后台支撑服务集, 关注点在 Node,保证每个Node 上都会运行一个此类的Pod,也可以通过 nodeSelector(将要被废弃) 选择特定的 node, 典型应用在 存储,日志,监控等服务  
StatefulSet | 有状态服务集,StatefulSet中的每个Pod的名字都是事先确定的,不能更改。典型如mysql,zookeeper, etcd 等  
Volume | 存储卷,作用于一个 Pod 内的所有容器  
PV与PVC(Persistent Volume 与 Persistent Volume Claim) | 抽象了存储,使得在配置Pod的逻辑里可以忽略对实际后台存储技术的配置, PV 定义了实际的存储, PVC 声明了需要使用什么规格的存储,pod 根据 PVC 的定义自动找到可用的 PV  
Node | Pod运行的物理节点,每个node都要有 kubelet 和 kubeproxy  
Secret | 密钥对象,保存和传递密码、密钥、认证凭证这些敏感信息的对象  
Namespace | 命名空间  
UserAccount 和 ServiceAccount | 用户账户和服务账户,用户帐户对应的是人的身份,人的身份与服务的namespace无关,所以用户账户是跨namespace的;而服务帐户对应的是一个运行中程序的身份,与特定namespace是相关的。  
RBAC | 访问授权,主要是引入了角色(Role)和角色绑定(RoleBinding)的抽象概念

### 入门
#### 为什么要给每一个 pod 初始一个 pause 容器
1. 以业务无关的 pause 容器的状态代表 pod 的状态
2. 方便 pod 中的容器共享网络和存储 

#### 理解最小单元 pod
1. pod 中任意一个容器停止,kubernetes 都会自动的重启该 pod
2. pod 所在节点宕机后,该节点的所有 pod 将重新调度到其他节点

#### Label Selector 的一些使用场景
1. kube-controller 通过 RC 定义的 LabelSelector 筛选要监控的 Pod 副本数,从而实现 Pod 副本数始终符合预期设定的自动控制流程
2. kube-proxy 通过 Service 的 Label Selector 选择对应的 Pod, 自动建立 Service 到 Pod 的请求转发路由表,实现负载均衡
3. 对 Node 定义特定Label, 并在 Pod 定义中使用 NodeSelector,实现 Pod 的定向调度

#### ReplicationController(RC)的一些特性与作用,Replica Set 与之相同
- 大部分情况下,通过定义 RC 实现 Pod 的管理
- RC 里包含完整的 Pod 定义模板
- RC 通过 Label Selector 实现对Pod 副本的自动控制
- 通过改变 RC 里的 Pod 副本数,可以实现 Pod 的扩容和缩容
- 通过改变 RC 里的 Pod 模板中的镜像版本,可以实现 Pod 的滚动升级
#### Replication Controller 和 Replica Set 的区别
Replica Set 支持基于集合的 Label selector (Set-based selector)  
Replication Controller 只支持基于等式的 Label Selector(equality-based selector)  

Replica Set 很少单独使用,它主要被 Deployment 这个更高层的资源对象使用.  
Replica Set 和 Department 逐步替代了 RC的作用

#### Deployment 的使用场景
- 创建一个 Deployment 来生层对应的 Replica Set 并完成副本的创建过程
- 检查 Deployment 状态看部署是否完成(Pod副本的数量是否达到预期的值)
- 更新 Deployment 以创建新的 Pod (比如镜像升级)
- 如果当前 Deployment 不稳定,则回滚到一个早先的 Deployment 版本
- 挂起或者恢复一个 Deployment

#### Horizontal Pod Autoscaler (HPA) 是什么?
HPA 也是一个资源对象, 它表示 Pod 横向自动扩容: 根据目标 Pod 的负载情况,自动的调整目标 Pod 的副本数.  
HPA 可以根据两行方式作为指标:  
1. CPUUtilizationPercentage, 表示目标 Pod 所有副本的 Cpu 利用率的平均值. 
2. 应用程序自定义的度量指标,比如 TPS 或 QPS      

注意:  
- Pod CPU 使用率来源于 heapster, 要预先安装
- 在 RC 或 Deployment 中的 Pod 必须定义 `resources.requests.cpu`

#### Kubernetes 里的"三种 IP"
##### NodeIP: Node 节点的 IP 地址
Kubernetes 集群中每个节点的物理网卡IP地址, Kubernetes 集群外的节点通过 NodeIP 访问 Kubernetes 集群中某个节点的服务.
##### PodIP: Pod 的 IP 地址
它是 Docker Engine 根据 docker0 网桥的IP地址段进行分配的,通常是一个虚拟的二层网络.
Kubernetes 里一个 Pod 里的容器访问另一个 Pod 里的容器,就是通过 PodIP 所在的虚拟二层网络进行通信,
而真实的 TCP/IP 流量则是通过 NodeIP 所在的物理网卡流出的.

##### ClusterIP: Service 的 IP 地址
虚拟的IP
- ClusterIP 仅仅作用于 Kubernetes Service 这个对象,并由 Kubernetes 管理和分配 IP 地址(来源于 ClusterIP 地址池)
- ClusterIP 无法并Ping, 因为没有一个"实体网络对象"来响应
- ClusterIP 只能结合 Service Port 组成一个具体的通信端口,单独的 ClusterIP 不具备 TCP/IP 通信的基础.
- 在 Kubernetes 集群中,NodeIP网,PodIP网与ClusterIP网之间的通信,采用的是 Kubernetes 自己设计的一种变成方式的特殊的路由规则

#### Service 的 NodePort 方式实现集群外部访问服务
实现方式: 在 Service 的 `spec` 中制定 `type` 为 `NodePort`, 并在 `spec.ports` 中定义 `nodePort`  

注意: 外部系统可以用kubernetes集群中任意一个 NodeIP + 具体NodePort 访问内部服务.

#### 定义在Pod上的Volume类型
##### emptyDir
emptyDir Volume 是在 Pod 分配到 Node 时创建的,Kubernetes 自动为其在宿主机上分配一个目录.
当 Pod 从 Node 上移除时, emptyDir 中的数据也会被永久删除.  

应用场景:
- 临时空间,某些应用程序运行时所需要的临时目录,且无需永久保留
- 长时间任务的中间过程 CheckPoint 的临时保存目录
- 一个容器需要从另一个容器中获取数据的目录(多容器共享目录)
##### hostPath
为Pod挂在宿主机上的文件或目录.  

应用场景:
- 容器应用程序生成的需要永久保存的日志文件
- 需要访问宿主机上Docker引擎内部数据结构的容器应用时,可以定义 hostPath 为 /var/lib/docker 目录

注意:  
- 在不同的 Node 上具有相同配置的 Pod 可能会因为宿主机上的目录和文件不同而导致对 Volume 上的目录和文件的访问结果不一致
- 如果使用了资源配额管理,则 Kubernetes 无法将 hostPath 在宿主机上使用的资源纳入管理

##### NFS 网络文件系统

##### 其它
- gcePersistentDick 谷歌公有云的永久磁盘
- awsElasticBlockStore 亚马逊公有云提供的 EBS Volume 存储 
- ...

#### Persistent Volume(PV) 与 Persistent Volume Claim(PVC)
PV 是一种资源对象; PVC 是创建 PV 的模板. 

- PV 只能是网络存储,不属于任何 Node, 但可以在每个 Node 上访问
- PV 不是定义在 Pod 上的,而是独立于 Pod 之外的定义
- PV 类型: NFS,RBD,GCE Persistent Disks,iSCSCI,AWS ElasticBlockStore,GlusterFS 

#### ConfigMap 供容器使用的典型用法和限制条件
##### 典型用法
- 生成为容器内的环境变量
- 设置容器启动命令的启动参数(需设置为环境变量)
- 以 Volume 的形式挂载为容器内部的文件或目录
##### 限制条件
- ConfigMap 必须在 Pod 之前创建
- ConfigMap 也可以定义为属于某个 Namespace, 只有处于相同 Namespaces 中的 Pod 可以引用它
- 只能用于被 Api Server 管理的 Pod 使用,静态 Pod 无法引用 ConfigMap
- Pod 对 ConfigMap 进行挂载(VolumeMount)时,只能被挂载为目录,而不是文件,且会覆盖该目录其他文件.如果要保留其他文件,可以先将 ConfigMap 挂载到临时目录,在通过启动脚本将配置文件复制到 实际配置目录下

#### Project Volume
Projected Volume,可以把它翻译为“投射数据卷”,Projected Volume是Kubernetes v1.11之后的新特性.  
在Kubernetes中，有几种特殊的Volume，它们存在的意义不是为了存放容器里的数据，也不是用来进行容器和宿主机之间的数据交换。这些特殊Volume的作用，是为容器提供预先定义好的数据。所以，从容器的角度来看，这些Volume里的信息就是仿佛是被Kubernetes“投射”（Project）进入容器当中的。这正是Projected Volume的含义。  
到目前为止，Kubernetes支持的Projected Volume一共有四种：
- Secret
- ConfigMap
- Downward API
- ServiceAccountToken: 保存 Service Account的授权信息和文件, 它只是一种特殊的 Secret 对象, kubernetes 提供了一个默认的 default Service Account,把Kubernetes客户端以容器的方式运行在集群里，然后使用default Service Account自动授权的方式，被称作“InClusterConfig”，是最推荐的进行Kubernetes API编程的授权方式。  


### Pod
#### Pod 的几种状态
- Pending: API Server 已经创建该 Pod, 但 Pod 内还有一个或多个容器的镜像没有创建,包括正在下载镜像的过程
- Running: Pod 内所有容器均已创建,且至少有一个容器处于运行,正在启动,或者正在重启状态
- Succeed: Pod 内所有容器均成功执行退出,且不会再重启
- Failed: Pod 内所有容器均已退出,但至少有一个容器退出为失败状态
- Unknown: 无法获取该Pod的状态,可能由于网络通信问题导致  

#### pod 的创建流程
1. 用户通过 REST API 创建一个 Pod
2. apiserver 将其写入 etcd
3. scheduluer 检测到未绑定 Node 的 Pod,开始调度并更新 Pod 的 Node 绑定
4. kubelet 检测到有新的 Pod 调度过来,通过 container runtime 运行该 Pod
5. kubelet 通过 container runtime 取到 Pod 状态,并更新到 apiserver 中
#### Pod 的重启策略(Restart Policy)
由Pod所在Node上的kubelet进行判断,当容器异常退出或者健康检查失败后,根据Pod设置的重启策略进行操作.  
重启策略包括:  
- Always: 容器失效时,自动重启
- OnFailure: 容器终止运行且退出码不为0时,自动重启
- Never: 不会重启  

用于管理 Pod 的控制器对Pod重启策略的要求:  
- RC 和 DaemonSet: 必须为 Always,保证容器持续运行
- Job: OnFailure 或 Never, 确保容器执行完后不再重启
- kubelet 命令行: 失效时自动重启,不管 RestartPolicy 设置为什么值,也不会对 Pod 进行健康检查

#### Pod 健康检查
- LivenessProbe 探针: 判断容器是否存活(running 状态),不存活则删除并重新创建容器, 如果容器不包含 LivenessProbe, 则始终认为是 "success"
- - ExecAction: 在容器内部执行一个命令,返回为0, 则表明容器健康
- - TcpSocketAction: 判断是否可以通过容器的 IP 和端口号建立TCP连接
- - HTTPGetAction: 判断容器的http服务的一个Get请求是否返回大于200小于400的状态码
- ReadinessProbe: 判断容器是否启动完成(ready状态), 可以接收请求,否则不接受来自 kubernetes Service 的流量

#### Pod 的调度
##### RC,RS,Deployment: 全自动调度
维护多份副本
##### DaemonSet: 特定场景调度,后台支撑服务集
用于管理在集群中每个 Node 上仅运行一份 Pod 的副本实例, 比如:  
- 在每个 Node 上运行一个 GlusterFS 存储或者 Ceph 存储的 daemon 进程
- 在每个 Node 上运行一个日志采集程序, 例如 fluentd 或者 logstach
- 在每个 Node 上运行一个健康程序,采集该Node的运行性能数据,例如 Prometheus Node Exporter, collectd, New Relic agent 或者 Ganglia gmond 等  

长期伺服型和批处理型服务的核心在业务应用,可能有些节点运行多个同类业务的
Pod,有些节点上又没有这类Pod运行;而后台支撑型服务的核心关注点在K8s集群中的
节点(物理机或虚拟机),要保证每个节点上都有一个此类Pod运行。节点可能是所有
集群节点也可能是通过nodeSelector选定的一些特定节点。典型的后台支撑型服务包
括,存储,日志和监控等在每个节点上支撑K8s集群运行的服务。

##### Job: 批处理调度
Job管理的Pod根据用户的设置把任务成功完成就自动退出了。成功完成的标志根据不同的
spec.completions策略而不同:单Pod型任务有一个Pod成功就标志完成;定数成功型任
务保证有N个任务全部成功;工作队列型任务根据应用确认的全局成功而标志成功。
###### Non-parallel Jobs
通常一个 Job 只启动一个 Pod,只有在Pod异常后,才会重启该Pod,Pod正常结束,Job也将结束

###### Parallel Jobs With a fixed completion count
- 并行 Job 会启动多个 Pod
- 当正常结束的 Pod 数量达到 `spec.completions` 时,Job结束.
- `spec.parallelism` 参数控制并行度,表示同时起送几个 Job 来处理 Work Item

每个 Pod 对应一个工作项,处理完一个,Pod就结束了,这种方式会大量的结束和开启 Pod

###### Parallel Jobs with a work queue
- 需要一个存放 Work item 的独立的 Queue
- 不能设置 `spec.completions` 参数
- 每个 Pod 能独立判断和决定是否还有任务项需要处理
- 如果某个 Pod 正常结束,则 Job 不会再启动新的 Pod,其他Pod 应该处于即将结束或者退出状态
- 所有Pod都结束了,且至少有一个 Pod 成功结束,则整个Job算成功结束  

每个 Pod 不断从对垒中拉取工作项并处理,知道队列为空,Pod退出执行,因此,这种情况下,只要有一个 Pod 成功结束,就意味着整个 Job 进入终止状态

#### 滚动升级(Rolling Update)的流程 todo
新建一个新的 RC: `new-rc.yaml`, 运行 `kubectl rolling-update <old-rc> -f new-rc.yaml`  

注意:  
- 新的 RC 的名称不能与旧的 RC 名称相同  
- 新的 RC 在 Selector 中应至少有一个 label 与旧的 RC 的 Label 不同,以标识新的RC

#### PodPreSet
PodPreset（Pod预设置）的功能 已经出现在了v1.11版本的Kubernetes中。
PodPreset里定义的内容，只会在Pod API对象被创建之前追加在这个对象本身上，而不会影响任何Pod的控制器的定义。

### Service
#### 普通 Service
RC、RS和Deployment只是保证了支撑服务的微服务Pod的数量, Service 解决如何访问这些服务的问题.每个Service会对应一个集群内部有效的虚拟IP,集群内部通过虚拟
IP访问一个服务。在K8s集群中微服务的负载均衡是由Kube-proxy实现的。Kube-proxy
是K8s集群内部的负载均衡器。它是一个分布式代理服务器,在K8s的每个节点上都有一
个;这一设计体现了它的伸缩性优势,需要访问服务的节点越多,提供负载均衡能力的
Kube-proxy就越多,高可用节点也随之增多。与之相比,我们平时在服务器端使用反向
代理作负载均衡,还要进一步解决反向代理的高可用问题。
#### 什么是 Headless Service   
在某些场景中,开发人员希望自己控制负载均衡的策略,不使用 Service 提供的默认负载均衡,这时就可以通过 Headless Service 实现.   

将 Service 的 Cluster 设置为 None,通过 Label Selector 将后端的 Pod 列表返回给调用的客户端,由客户端程序自己实现负载均衡,确定范文哪一个后端 Pod

#### 什么是无 Label Selector 的服务  
某些环境中,kubernetes 中的服务需要连接一个外部数据库,或者连接另一个集群或namespace 的服务,这时可以通过创建一个无 Label Selector 的 Service 实现.  

定义一个无LabelSelector的Service,就无法选择后端 Pod, 因此需要先手动创建一个 Endpoint,

#### kubernetes 外部访问 Pod 或 Service 的方式

##### 将容器应用的端口号映射到物理机(不推荐,因为Pod的IP和所在的Node是随时会变的)
1. 设置容器级别的 hostPort, 将容器应用的端口号映射到物理机上,然后通过物理机 IP + hostPort 就可以访问Pod内的服务  
2. 设置 Pod 级别的 hostNetwork= true, 该 Pod 中所在的容器端口号都会被映射到物理机上.

##### 将 Service 的端口号映射到物理机 
1. 通过设置 `spec.type=NodePort`,且在 `spec.ports.port.nodePort` 指定映射到物理机的端口, 通过 NodeIP + NodePort 可以访问服务
2. 设置 LoadBalancer,映射到负载均衡的IP地址,一般仅用于云平台

#### Ingress: HTTP 7 层路由机制
对于基于 http 的服务来说,仅仅通过 Service 的 IP:Port 形式不能满足不同url对应不同服务的需求.  
比如:
- 对 http://website/api 的访问要路由到 名为 api 的 Service(http://api:80)
- 对 http://website/web 的访问要路由到 名为 web 的 Service(http://web:80)
- 对 http://website/docs 的访问要路由到 名为 docs 的 Service(http://docs:80)  

这种场景可以用 Ingress 解决, 步骤:  
##### 创建 Ingress Controller
Ingress Controller 实现基于不同 HTTP URL 向后转发的负载分发规则,有的公有云也提供了这种类型的 LoadBalancer,可以将其设置为 Ingress Controller.  

可以用 nginx 实现一个 Ingress Controller.  

##### 定义 Ingress

### Kubernetes API Server
- 提供了各类资源对象的curd及watch 等 http rest 接口,是数据交互和通信的中心枢纽
- 是集群管理的API入口
- 是资源配额控制的入口
- 提供了完备的集群安全机制
- kubectl 就是通过调用 kube-apiserver 提供的 rest 接口来进行操作的,因此,也可以使用 curl 替代 kubectl

### Controller Manager 管理控制中心
负责集群内的Node,Pod副本,Endpoint,Namespace,ServiceAccount,ResourceQuota 等的管理,  
它会及时发现故障并自动修复,确保集群始终处于预期的工作状态,是核心管理者.    

是Kubernetes 的大脑, 通过 apiserver 监控整个集群的状态,并确保集群处于预期的工
作状态。


#### Replication Controller: 副本控制器, 注意区别同样称为 Replication Controller(简称 RC) 的一种资源对象,
职责:  
- 自动调度: 确保当前集群中有且仅有 N 个Pod实例
- 弹性伸缩: 通过调整 replicas 属性实现系统扩容或缩容
- 滚动更新: 通过修改 RC 中 Pod 模板(主要是镜像版本)来实现系统的更新,通过创建一个新的 RC,实现滚动更新,新RC的副本数逐步加1,旧 RC 的副本数逐步减1

#### Node Controller  

kubelet 进程在启动时通过 API server 注册自身节点信息,并定时汇报状态信息.    

NodeController 通过 API Server 实时获取Node信息,实现管理和监控集群中的各个 Node 节点的相关控制功能.  

#### ResourceQuota Controller 资源配额控制器
确保指定的资源对象在任何时候都不会超量占用系统物理资源,确保集群的稳定性.  

目前,支持三个层次的资源配额管理:  
- 容器级别,对 cpu 和 memory 进行限制
- Pod 级别,对 Pod 内所有容器的可用资源进行限制(通过 LimitRanger 设置)
- Namespace 级别,包括 Pod 数量,Replication Controller 数量,Service 数量,ResourceQuota 数量,Secret 数量,可是持有的 Persistent Volume 数量(通过 ResourceQuota 设置)

#### Namespace Controller  

管理 Namespace 的 创建和删除, 删除的同时,会删除该 Namespace 下的各种资源对象

#### Endpoint Controller
Endpoints 表示一个 Service 对应的所有 Pod 副本的访问地址, EndpointsController 就是负责生成和维护所有 Endpoints 对象的控制器. 它负责
监听 Service 和 对应副本的变化:  
- 如果 Service 被删除,则删除和该 Service 同名的 Endpoints 对象  
- 如果 Service 被创建,则根据 Service 信息获取 Pod 列表,然后创建或者更新 Service 对应的 Endpoints 对象  
- 如果检测到 Pod 时间,则更新它所对应的 Service 的 Endpoints 对象  

Endpoints 对应被每个 Node 上的 kube-proxy 进程使用,kube-proxy 进程获取每个 Service 的 Endpoints, 实现了 Service 的负载均衡.

#### Service Controller  

它其实是 Kubernetes 集群与外部的一个接口控制器,Service Controller 监听 Service 的变化,如果是一个 LoadBalancer 类型的Service,就确保
外部云平台上该 Service 对应的 LoadBalancer 实例被相应的创建,删除以及更新路由转发表.  

### kubernetes Scheduler  

Kubernetes Scheduler 在整个系统中承担了"承上启下"的重要功能,"承上"是指它负责接收 Controller Manager 创建的新 Pod, 为其安排一个落脚的"家"-目标Node;
"启下"是指安置工作完成后,目标Node上的kubelet 服务进程接管后继工作,负责Pod生命周期中的"下半生".  

简单的说,就是通过调度算法调度,为待调度Pod列表的每个Pod从Node列表中选择一个最合适的Node.  

随后,目标Node上的kubelet通过API Server监听到的Kubernetes Scheduler 产生的 Pod 绑定事件,然后获取对应的 Pod 清单,下载 Image 镜像,并启动容器.  

大概步骤:  
- 预选调度过程: 遍历所有目标Node,筛选出符合要求的候选节点.  
- 确定最优节点: 在预选过程产生的候选节点上,采用优选策略计算出每个候选节点的积分,积分最高者成为目标Node

#### 预选策略
- NoDiskConflict: 判断待调度的Pod的GCEPersistentDisk 或 AWSElasticBlockStore 和备选Node中已存在的 Pod 是否存在冲突.   
- PodFitsResources: 判断备选Node的资源是否满足备选Pod的需求  
- PodSelectorMatches: 判断备选Node是否包含备选Pod的 `spec.nodeSelector`指定的标签  
- PodFitsHost: 判断备选Pod的`spec.nodeName`所指定的节点名称和备选Node的名称是否一致  
- CheckNodeLabelPresence
- CheckServiceAffinity  
- PodFitsPorts

#### 优选策略
- LeastRequestedPriority: 选出资源消耗最小的节点  
- CalculateNodeLabelPriority: 判断策略列出的标签在备选节点中存在时,是否选择该备选节点.
- BalancedResourceAllocation: 选出各项资源使用率最均衡的节点.  

### kubelet  

Kubelet 用于处理 Master 节点下发到本节点的任务,管理 Pod 及Pod中的容器,并在 API Server 上注册节点自身信息,定期向 Master 节点汇报节点资源的使用情况,并
通过 cAdvisor 监控容器和节点资源.  

#### kubelet 处理创建和修改Pod任务  
1. 为该 Pod 创建一个数据目录
2. 从 APIServer 读取该Pod清单
3. 为该 Pod 挂载外部卷(External Volume)
4. 下载 Pod 用到的 Secret
5. 检查已经运行在节点中的 Pod,如果该 Pod 没有容器或 Pause 容器没有启动,则先停止 Pod里 所有容器的进程.如果在 Pod 中有需要删除的容器,则删除这些容器.
6. 用 'kubernetes/pause' 镜像为每个 Pod 创建一个容器.该 Pause 容器用于接管 Pod 中所有其他容器的网络.每创建一个新的 Pod,kubelet 都会先创建一个 Pause 容器,然后创建其他容器
7. 为 Pod 中的每个容器做如下处理:  
7.1 为容器计算一个 hash 值,然后用容器的名字去查询对应的 Docker 容器的 hash 值.若查找到容器,且两者不同,则停止Docker中的容器进程,并停止与之关联的 Pause 容器的进程;若两者相同,则不做任何处理.  
7.2 如果容器被终止了,且容器没有指定的 restartPolicy,则不做任何处理  
7.3 调用 DockerClient 下载容器镜像,调用 Docker Client 运行容器.

#### kubelet 健康检查

- LivenessProbe 探针: 判断容器是否存活(running 状态),不存活则删除并重新创建容器, 如果容器不包含 LivenessProbe, 则始终认为是 "success"
- - ExecAction: 在容器内部执行一个命令,返回为0, 则表明容器健康
- - TcpSocketAction: 判断是否可以通过容器的 IP 和端口号建立TCP连接
- - HTTPGetAction: 判断容器的http服务的一个Get请求是否返回大于200小于400的状态码
- ReadinessProbe: 判断容器是否启动完成(ready状态), 可以接收请求,否则不接受来自 kubernetes Service 的流量 

1. 只要Pod的restartPolicy指定的策略允许重启异常的容器（比如：Always），那么这个Pod就会保持Running状态，并进行容器重启。否则，Pod就会进入Failed状态 。  
2. 对于包含多个容器的Pod，只有它里面所有的容器都进入异常状态后，Pod才会进入Failed状态。在此之前，Pod都是Running状态。

#### Kubelet Eviction(驱逐)  

#### CRI(Container Runtime),OCI(Open Container Initiative),  CNI(Container Networking Interface), CSI(Container Storage Interface)。
Kubelet 通过 CRI(Container Runtime Interface) 与容器运行时交互,以管理镜像和容器。 
CRI 是一个grpc接口,kubelet 实现grpc客户端, 容器运行时需要实现grpc服务端(通常称为 CRI shim).
而具体的容器运行时,则通过OCI(Open Container Initiative)开放容器标准与底层的 Linux 操作系统进行交互,
即把 CRI 请求翻译成对 Linux 操作系统的调用(操作 Linux Namespace 和 Cgroups).  

kubelet 还会调用网络插件和存储插件为容器配置网络和持久化存储,这两个插件与 kubelet 进行交互的接口,分别是  CNI(Container Networking Interface), CSI(Container Storage Interface)。



### kube-proxy  
Service 是对一组 Pod 的抽象,它会根据访问策略(负载均衡)来访问这组Pod,Service 只是一个概念,而真正将 Service 的作用落实的背后是 kube-proxy 服务进程.  

每个 Node 上都会运行一个 kube-proxy 服务进程,它监听 API server 中 service 和 endpoint 的变化情况,它可以看作是 Service 的透明代理兼负载均衡器,将访问Service 的请求转发到后端的某个 Pod 上 .  

Service 的 ClusterIP 与 NodePort 等概念是 kube-proxy 服务通过 Iptables 的 NAT 转换实现的.   

访问 Service 的请求,不论是 ClusterIP + TargetPort 的方式,还是 NodeIP + NodePort 的方式,都被Node的Iptables 规则重定向到 kube-proxy 监听 Service 服务代理端口.   

kube-proxy 可以直接运行在物理机上,也可以以 static pod 或者 daemonset 的方式运行。    

仅支持 TCP 和 UDP,不支持 HTTP 路由,并且也没有健康检查机制。这些可以通过自定义 Ingress Controller 的方法来解决。

#### kube-proxy 原理  
kube-proxy 查询和监听 API Server 中 Service 与 Endpoints 的变化, 为每个Service 建立一个"服务代理对象(kube-proxy内部的一个数据结构)",在 LoadBalancer 上保存了Service到Endpoints的动态转发路由表,
由RoundRobin算法和Session保持(SessionAffinity)两个特性决定路由到哪个Endpoint.   

##### 针对发生变化的 Service 列表,kube-proxy 会逐个处理,流程如下:  
- 如果Service没有设置ClusterIP,则不做任何处理,否则,获取该 Service 的所有端口定义列表(spec.ports域)  
- 逐个读取端口信息,根据端口名称,Service名称和Namespace判断本地是否已经存在对应的服务代理对象,没有则新建;如果存在并且Service 端口被修改过,则先删除Iptables中和该Service端口相关的规则,关闭服务代理对象,然后走新建流程:分配服务代理对象并创建相关Iptables规则  
- 更新负载均衡器中对应Service的转发地址列表,对于新建的Service,确定转发时的会话保持策略.  
- 对于已经删除的Service则进行清理.    

针对Endpoint的变化,kube-proxy 会自动更新负载均衡器中对应的 Service 的转发地址列表  

##### kube-proxy 对 Iptables 做的一些操作  

kube-proxy 启动时监听到 Service 或 Endpoint变化后,会在本机Iptables的NAT表中添加4条规则:  
1. KUBE-PROTALS-CONTAINER: 从容器中通过 ClusterIP + TargetPort 访问Service  
2. KUBE-PROTALS-HOST: 从主机中通过 ClusterIP + TargetPort 访问 Service  
3. KUBE-NODEPORT-CONTAINER: 从容器中通过 NodeIP + NodePort 访问 Service  
4. KUBE-NODEPORT-HOST: 从主机中通过 NodeIP + NodePort 访问 Service

todo: iptables 细节  

### kubernetes DNS  
推荐使用 CoreDNS(从 v1.13 开始) 替代 kube-dns 为集群提供 DNS 服务
  

### Kubernetes 安全机制  
- Authentication 认证
- Authorization 授权
- Admission Control 准入控制
- Service Account: 内部Pod调用服务的认证方式
- Secret 私密凭据

### 网络插件
  
特性: Pod 内的所有容器共享一个网络栈, IP-Per-Pod, 集群内的Pod可以互相直接通过对方IP访问对方  

为了满足特性,kubernetes 对集群的网络有如下要求:  
- 所有容器都可以在不用 NAT 的方式下同别的容器通信  
- 所有Node和所有容器之间都可以在无需 NAT 的方式下互相访问
- 容器的地址和别人看到的地址是同一个地址  

#### CNI (Container Network Interface) 容器网络接口
Container Network Interface (CNI) 最早是由CoreOS发起的容器网络规范,是
Kubernetes网络插件的基础。其基本思想为:Container Runtime在创建容器时,先创建
好network namespace,然后调用CNI插件为这个netns配置网络,其后再启动容器内的
进程。现已加入CNCF,成为CNCF主推的网络模型。  

Kubernetes Pod 中的其他容器都是Pod所属pause容器的网络,创建过程为:
1. kubelet 先创建pause容器生成network namespace
2. 调用网络CNI driver
3. CNI driver 根据配置调用具体的cni 插件
4. cni 插件给pause 容器配置网络
5. pod 中其他的容器都使用 pause 容器的网络

##### Flannel
Flannel通过给每台宿主机分配一个子网的方式为容器提供虚拟网络,它基于Linux
TUN/TAP,使用UDP封装IP包来创建overlay网络,并借助etcd维护网络的分配情况。  
控制平面上host本地的flanneld负责从远端的ETCD集群同步本地和其它host上的subnet
信息,并为POD分配IP地址。数据平面flannel通过Backend(比如UDP封装)来实现L3
Overlay,既可以选择一般的TUN设备又可以选择VxLAN设备。  

##### Calico

### CRI (Container Runtime Interface) 容器运行时接口
Kubelet 通过 Container Runtime Interface (CRI) 与容器运行时交互,以管理镜像和容器。  

CRI 是一个grpc接口,kubelet 实现grpc客户端, 容器运行时需要实现grpc服务端(通常称为 CRI shim)

### CSI (Container Storage Interface) 容器存储接口  

类似于 CRI,CSI 也是基于 gRPC 实现。


### Kubernetes 资源管理
  
#### 计算资源管理 Compute Resources
计算资源配置项分为 Requests(下限) 和 Limits(上限)  
- Requests 和 limits 都是可选的,有默认值
- Requests 如果没有配置, 默认会被设置为等于 Limits
- Limits >= Requests  
- Pod 的资源限制参数是所有Pod 中所有容器对应配置的总和  
- 调度器在调度时,首先要确保调度后该 node 上的所有 pod 的cpu和memory 的Requests 总和不超过该 node 的提供给 pod 的最大容量  
- 

**CPU:**  
单位: 0.1 = 100m, 推荐使用形如 100m 的 millicpu 作为计量单位  
**Memory:**  
默认单位为字节数(bytes), 同时支持多种单位.       
注意区分十进制和二进制单位的不同:
- 十进制: 1KB = 1000 bytes = 8000 bits  
- 二进制: 1KiB = 2^10 bytes = 1024 bytes = 8192 bits  

#### 资源配置范围管理 LimitRange(资源对象)
LimitRange 是一种资源对象,作用于一个 Namespace.


#### 服务质量管理 Resource Qos
Qos 体系,用于保证高可靠的 Pod 可以申请可靠资源,而一些不需要高可靠性的Pod可以申请可靠性较低的资源.  

- Requests == Limits, 完全可靠
- Requests < Limits, 小于 Requests 部分的资源完全可靠,超出 Requests 的部分不可靠

**可压缩资源 CPU:**
- 空闲CPU按照容器的Requests值的比例分配
- 如果cpu没有配置limits,那么Pod会尝试抢占所有空闲的CPU
**不可压缩资源 Memory:**  
- 同一node上的Pod发生竞争或有新的Pod调度到该node上时,内存使用量超过 Requests 的Pod, 可能会被 kill
- Pod 的内存使用量超过 limits 时,会kill 掉 Pod 中内存使用最多的容器  

**Pod 的三种Qos级别:**
- Guaranteed (完全可靠的): Pod 中所有容器都定义了 Requests 和 Limits,并且它们的值均不为0且相等,可以只定义Limits,因为Requests未定义时默认为 Limits
- Burstable (弹性波动,较可靠的): Pod 中所有容器都未定义 Requests 和 Limits
- Best Effort (尽力而为,不太可靠的): 既不是 guaranteed,又不是 burstable 的 ,就是 best effort.  

#### 资源的配额管理 (Resource Quotas)  
ResourceQuota 是一种资源对象,它可以定义一项资源配额,为每一个Namespace提供一种总体的资源使用限制:  
- 限制某种类型的对象的总数目上限  
- 设置 Namespace 中 Pod 可以使用的计算资源的总上限.





## 注意
### 前台运行启动命令
kubernetes 要求我们自己创建的docker镜像以一个前台命令作为启动命令,如果在后台运行,比如 `nohup ./start,sh &`, 该命令执行完后,会销毁该Pod.  

对于无法改造为前台执行的应用,可以使用 supervisor.

### Endpoint
PodIP + containerPort = Endpoint, 一个 Pod 可以有多个 Endpoint

### 删除 RC 控制的 pod
删除一个 RC 不会影响它所创建的 Pod, 如果想删除一个 RC 所控制的 Pod, 需要将该 RC 的 replicas 设置为 0, 这样所有的 Pod 副本都会被自动删除.    

### 其他  
- 单进程意思不是只能运行一个进程，而是只有一个进程是可控的。
