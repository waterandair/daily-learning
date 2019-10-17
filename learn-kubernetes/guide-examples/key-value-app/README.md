## key-value-app 示例
## 说明 
译自 https://github.com/kubernetes/examples/tree/master/guestbook-go, 做了一些修改:  
- 使用 yaml 文件描述kubernetes资源对象,替代 json
- 使用 Deployment 替换 Replication Controller
- 使用 `kubectl apply -f` 替换 `kubectl create -f`
- 包含镜像的构建过程
- 用命令行的方式替换了web界面的方式,返回了 redis server 的详细信息,以及各个 app 的 pod_ip

这个实例展示了使用Kubernetes和Docker构建一个简单的多层web应用.这个应用包含web前端,redis-master 做存储,redis-slave 做副本,会为每个模块都创建
Kubernetes 的副本控制器,Pods,和 Services.


##### 目录

 * [第零步: 前提准备](#step-zero)
 * [第一步: 创建 Redis master 的 Pod](#step-one)
 * [第二步: 创建 Redis Master 的 Service](#step-two)
 * [第三步: 创建 Redis slave 的 Pods ](#step-three)
 * [第四步: 创建 Redis slave 的 Service](#step-four)
 * [第五步: 写代码实现 key-value-app, 并构建镜像](#step-five)
 * [第六步: 创建 key-value-app 的 pods](#step-six)
 * [第七步: 创建 key-value-app 的 Service](#step-seven)
 * [第八步: 使用 curl 测试 key-value-app](#step-eight)
 * [第九步: 清理](#step-nine)

### 第零步: 前提准备 <a id="step-zero"></a>
这个示例假设你已有了一个可以工作的 kubernetes 集群,可以在这里查看创建集群的细节[Getting Started Guides](https://kubernetes.io/docs/setup/)

**单机kubernetes:** 为了快速在本地学习 kubernetes, 推荐使用 [microk8s](https://microk8s.io)

**注意:** 可以查看这里全面了解 `kubectl` 命令, 包括他们的选项和描述[kubectl CLI reference](https://kubernetes.io/docs/user-guide/kubectl-overview/).  

### 第一步: 创建 Redis master 的 Pod<a id="step-one"></a>

使用 `./redis-master-rc.yaml` 去创建一个 [replication controller](https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/) 和一个 redis master 的 [pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/). 
Pod 在容器中运行 redis k-v 服务. 推荐使用 RC(Replication Controller) 去运行长期运行的应用, 就算只有一个副本也推荐使用 RC 定义, kubernetes V1.13 以后,更推荐使用一种新的资源对象 Deployment, 它们都可以使应用方便的使用 kubernetes 自动恢复机制

1. 运行  `kubectl apply -f` *`filename`* command:

    ```console
    $ kubectl apply -f redis-master-deploy.yaml
    deployment.apps/redis-master 
    ```

2. 验证 redis-master 的控制器是否启动, 执行 `kubectl get deploy` 命令列出所有在kubernetes集群中创建的 Deployment (如果没有指定 `--namespace`, 将会使用默认命名空间 `default`):

    ```console
    $ kubectl get deploy
    NAME           READY   UP-TO-DATE   AVAILABLE   AGE
    redis-master   1/1     1            1           179m
    ...
    ```

    运行结果: Deployment 创建了一个 Redis Master Pod, 并且已经处于 REDAY 状态

3. 验证 redis-master 的 Pod 是否启动, 可以指定命令 `kubectl get pods` 列出集群中被创建的 Pods:

    ```console
    $ kubectl get pods
    NAME                            READY   STATUS    RESTARTS   AGE
    redis-master-5ffcc48fc8-4cbxt   1/1     Running   0          3h3m
    ...
    ```

    运行结果: 可以看到Pod已经被创建,并且处于了 Running 状态, 这一过程可能需要等30秒.

4. 为了验证 redis-master Pod 里的容器已经在运行, 可以登录到该物理节点执行 `docker ps`, 也可以执行一个`kubectl exec <pod-name> -c <container-name> date`命令,以判断它是否存在

    ```console
    $ kubectl exec redis-master-5ffcc48fc8-4cbxt -c redis-master hostname
      redis-master-5ffcc48fc8-4cbxt
    ```
   
   运行结果: `hostname` 命令已经在目标容器上正确的执行,并且可以发现一个有趣的现象,该容器的 hostname 就是该 Pod 的 Name.

### 第二步: 创建 Redis Master 的 Service <a id="step-two"></a>
Kubernetes 的 [Service](https://kubernetes.io/docs/concepts/services-networking/service/) 资源对象是一个命名的负载均衡器,它可以代理一个或多个 Pod 的流量.
集群中的 Pod 可以通过环境变量或 DNS 发现并访问 Service. Service 通过 Pod 的 Labels 发现它需要代理的 Pods.在第一步中创建的 Pod 包含两个标签 `app=redis` 和 `role=master`.
Service 的 `selector` 字段决定哪个Pod 将会接收到来自访问 Service 的流量.

1. 使用 [redis-master-sv.yaml](redis-master-svc.yaml) 文件在集群中创建一个文件 `kubectl apply -f` *`filename`* command:

    ```console
    $ kubectl apply -f redis-master-sv.yaml
    service/redis-master configured
    ```

2. 验证 service 是否被创建, 可以执行 `kubectl get svc` 查看所有services:

    ```console
    $ kubectl get svc
       NAME           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
       kubernetes     ClusterIP   10.152.183.1     <none>        443/TCP    40d
       redis-master   ClusterIP   10.152.183.226   <none>        6379/TCP   20d
    ...
    ```

    运行结果: 所有 `redis-master` service 选择的 Pod 可以看到, `redis-master` Service 运行在 `6379` 端口(`可以在Pod 中通过环境变量 
    $REDIS_MASTER_SERVICE_HOST` 查看). 
   
   
   ```
    # 执行命令查看 REDIS_MASTER_SERVICE_PORT
   $ kubectl exec redis-master-5ffcc48fc8-4cbxt -c redis-master env | grep REDIS_MASTER_SERVICE_PORT
     REDIS_MASTER_SERVICE_PORT=6379
   ```

### 第三步: 创建 Redis slave 的 Pods <a id="step-three"></a>

之前创建了只有一个pod副本的 redis-master 服务, 接下来创建有多个Pod副本的 redis-slave , 在 Kubernetes 中, Deployment 负载管理 Pod 的多个实例.

1. 构建 redis-slave 镜像  
Dockerfile 文件路径: `./docker/redis-slave/Dockerfile`, 这个镜像的主要操作是:
- 修改 bind 配置, 改为 bind 0.0.0.0 , 表示允许其他主机访问redis
- 修改 slaveof 配置, 表示是 redis 主节点 $REDIS_MASTER_SERVICE_HOST:$REDIS_MASTER_SERVICE_PORT 的从节点, 这两个环境变量,是 kubernetes 创建 redis-master Service 时在集群中创建的,它们会出现在每一个 Pod 中
- 使用指定的配置文件启动 redis

```dockerfile
FROM redis:5.0.6-alpine3.10

RUN cd /tmp && \
    wget http://download.redis.io/redis-stable/redis.conf && \
    mkdir -p /etc/redis && \
    cp redis.conf /etc/redis/ && \
    touch /etc/redis/run.sh && \
    echo "sed -i 's,bind 127.0.0.1,bind 0.0.0.0,g' /etc/redis/redis.conf" >> /etc/redis/run.sh && \
    echo "sed -i '/^bind 0.0.0.0$/aslaveof '"\$REDIS_MASTER_SERVICE_HOST"' '"\$REDIS_MASTER_SERVICE_PORT"'' /etc/redis/redis.conf" >> /etc/redis/run.sh && \
    echo "redis-server /etc/redis/redis.conf" >> /etc/redis/run.sh && \
    chmod 755 /etc/redis/run.sh && \
    chown -R redis:redis /etc/redis

EXPOSE 6379/tcp

CMD ["/etc/redis/run.sh"]
```

注意: 在 Dockerfile 的 RUN 指令是在构建镜像时执行的, 所有无法获取到容器的环境变量,所以将修改redis配置文件的命令写入脚本,在容器启动时执行.

2. 使用 [redis-slave-deploy.yaml](redis-slave-deploy.yaml) 运行命令 `kubectl apply -f` *`filename`* 创建 redis-slave Deployment:

    ```console
    $ kubectl apply -f redis-slave-deploy.yaml 
      deployment.apps/redis-slave created
    ```

3. 验证 redis-slave Deployment 正确运行, 执行 `kubectl get deploy`:

    ```console
    $ kubectl get deploy
   NAME           READY   UP-TO-DATE   AVAILABLE   AGE
   redis-master   1/1     1            1           19h
   redis-slave    2/2     2            2           3m4s
    ```

    运行结果: redis-slave Deployment 创建了两个 redis-salve Pod, 这两个 Pod 从环境变量中读取出 redis-master 地址在启动时作为 slave 连接到 master . 因为集群中开启了 kube-dns, 所以也可以通过redis master 的服务名访问到 master, 这里即为: `redis-master:6379`.


4. 为了验证redis的主从连接成功,可以运行一下命令To verify that the Redis master and slaves pods are running, run the `kubectl get pods` command:

    首先获取到刚刚创建的 pods, 可以看到有一个主节点和两个从节点:
    ```console
    $ kubectl get pods
      NAME                            READY   STATUS    RESTARTS   AGE
      redis-master-5ffcc48fc8-rqttr   1/1     Running   0          33m
      redis-slave-c97769b97-2rxkc     1/1     Running   0          33m
      redis-slave-c97769b97-cnbrm     1/1     Running   0          33m
    ...
    ```
   在两个终端中分别使用 `kubectl exec` 命令连接到具体的容器中:  
   terminal-1:
   ```
   $ kubectl exec -ti redis-master-5ffcc48fc8-rqttr  -c redis-master /bin/bash
   root@redis-master-5ffcc48fc8-rqttr:/data#
   ```
   terminal-2:
   ```
   $ kubectl exec -ti redis-slave-c97769b97-2rxkc  -c redis-slave /bin/sh
   /data 
   ```
   分别在两个终端中运行 `redis-cli`, 就可以连接上redis的主节点和从节点,之后就可以在其中执行 redis 命令, 以此快速验证主从节点可以顺利同步数据.  
   在容器中,还可以运行 env 查看 kubernetes 为容器设置的环境变量
   
### 第四步: 创建 Redis slave的 Service <a id="step-four"></a>
我们的应用需要从 redis slave 节点中读取数据,以此实现读写分离,所以需要在 kubernetes 为 redis 的从节点创建一个 Service, 通过这个 Service 可以代理到所有的从节点,并具备负载均衡功能.

1. 使用 [redis-slave-svc.yaml](redis-slave-svc.yaml) 创建 redis-salve service :

    ```console
    $ kubectl apply -f redis-slave-svc.yaml
    services/redis-slave
    ```

2. 验证 redis-slave service 是否创建成功 :

    ```console
    $ kubectl get svc
      NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
      kubernetes     ClusterIP   10.152.183.1    <none>        443/TCP    55d
      redis-master   ClusterIP   10.152.183.44   <none>        6379/TCP   53m
      redis-slave    ClusterIP   10.152.183.64   <none>        6379/TCP   76s
    ```

    结果: redis-salve 服务已经创建成功,在定义 Service 时建议为其定意思合适的 label,以便以后可以很方便的定位到该 Service.
    
### 第五步: 写代码实现 key-value-app, 并构建镜像 <a id="step-five"></a>
数据写入到 redis 主节点, 从 redis 从节点中读取,为了方便查看效果,写一个简单的 [http 服务](./docker/app/main.go), 在这个服务中初始化了两个 redis 客户端,分别用域名的方式
指向了 `redis-master:6379` 和 `redis-slave:6379`, 在当前的 kubernetes 环境中, 有两个 redis 从节点, 通过域名`redis-slave`的方式访问从节点,可以直接使用 kubernetes Service
提供的负载均衡的功能,在代码中 http 服务调用了 redis 服务的 info 接口,可以通过其返回信息查看服务负载均衡的情况.    

编译代码 `CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -v -o app main.go `, 并使用 `./docker/app/Dockerfile` 构建镜像 `docker build -t waterandair/key-value-app ./docker/app/Dockerfile`.  

注意: 因为使用的基础镜像是 alpine, 所以在编译 go 代码的时候一定要加 `CGO_ENABLED=0`,这样就能强制 Go 采用纯静态编译.
 
### 第六步: 创建 key-value-app 的 pods <a id="step-six"></a>
1. 使用 [key-value-app-deploy.yaml](key-value-app-deploy.yaml) 文件创建 key-value-app 的 Deployment:

    ```console
    $ kubectl apply -f key-value-app-deploy.yaml       
      deployment.apps/key-value-app created
   
    ```


2. 验证 key-value-app 的 Deployment 和 Pod 是否创建成功

    ```console
    $ kubectl get deploy              
      NAME            READY   UP-TO-DATE   AVAILABLE   AGE
      key-value-app   3/3     3            3           4m19s
      redis-master    1/1     1            1           5h23m
      redis-slave     2/2     2            2           5h23m
    $ guestbook-go git:(master) ✗ kubectl get pods  
      NAME                             READY   STATUS    RESTARTS   AGE
      key-value-app-7b7d944cbd-9vkhh   1/1     Running   0          4m22s
      key-value-app-7b7d944cbd-hj9px   1/1     Running   0          4m22s
      key-value-app-7b7d944cbd-r4prd   1/1     Running   0          4m22s
      redis-master-5ffcc48fc8-mkzj8    1/1     Running   0          5h23m
      redis-slave-c97769b97-cz698      1/1     Running   2          5h23m
      redis-slave-c97769b97-dfdhj      1/1     Running   2          5h23m

    ```

    结果: 可以看到在 kubernetes 集群中有一个单节点的 redis-master, 两个节点的 redis-slave, 三个节点的 key-value-app 

### 第七步: 创建 key-value-app 的 Service <a id="step-seven"></a>

创建 `key-value-app` 的 Service, 和之前创建的 Service 不同, 之前的 Service 只能在 kubernetes 集群内被访问到,但是 key-value-app 
的 Service 需要能被集群外部的请求访问到,这一点可以通过指定 Service 的 `spec.type` 为 `NodePort`, 并把 `spec.ports.nodePort` 的值设置为一个大于 30000 的值,
这样外部请求就可以通过地址 `物理节点IP:nodePort` 访问到 Kubernetes 内的 Service  

1. 使用 [key-value-app-svc.yaml](key-value-app-svc.yaml) 文件创建一个 NotePort 类型的 Service :

    ```console
    $ kubectl apply -f key-value-app-svc.yaml
    ```
   
2. 验证 Service 是否创建成功:

    ```console
    $ kubectl get svc                        
      NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
      key-value-app   NodePort    10.152.183.54    <none>        80:30003/TCP   6s
      kubernetes      ClusterIP   10.152.183.1     <none>        443/TCP        60d
      redis-master    ClusterIP   10.152.183.232   <none>        6379/TCP       24h
      redis-slave     ClusterIP   10.152.183.183   <none>        6379/TCP       24h
    ...
    ```

    结果: 可以看到名为 key-value-app 的 Service 被成功创建, 并且可以通过物理节点的 30003 端口访问到 Service 的 80 端口.

### 第八步: 使用 curl 测试 key-value-app <a id="step-eight"></a>
打开一个终端,选择 kubernetes 中任意一个集群某个节点的 IP, 使用 ctrl 向 `IP:30003` 发送请求,如果是本地测试,就是向 `127.0.0.1:30003` 发送请求:

1. 发送 POST 请求向 redis-master 中添加一个 key
```
$ curl -H "Content-type: application/json" -X POST -d '{"key":"key_1","value":"value_1"}' 127.0.0.1:30003/set
{
    "key":"key_1",
    "value":"value_1",
    "redis_replication":"
        # Replication\r\n
            role:master\r\n
            connected_slaves:2\r\n
                slave0:ip=10.1.37.1,port=6379,state=online,offset=88661,lag=1\r\n
                slave1:ip=10.1.37.1,port=6379,state=online,offset=88661,lag=0\r\n
            master_replid:96e151af1ceabb08e578123751362e53dd8a9054\r\n
            master_replid2:0000000000000000000000000000000000000000\r\n
            master_repl_offset:88712\r\nsecond_repl_offset:-1\r\n
            repl_backlog_active:1\r\nrepl_backlog_size:1048576\r\n
            repl_backlog_first_byte_offset:1\r\nrepl_backlog_histlen:88712\r\n",
    "action":"SET",
    "pod_ip":"10.1.37.13"
}

``` 

2. 发送 GET 请求向 redis-slave 获取一个 key
```
$ curl -X GET 127.0.0.1:30003/get?key=key_1
{
    "key":"key_1",
    "value":"get key_1: value_1",
    "redis_replication":"
        # Replication\r\n
            role:slave\r\n
            master_host:10.152.183.182\r\n
            master_port:6379\r\n
            master_link_status:up\r\n
            master_last_io_seconds_ago:6\r\n
            master_sync_in_progress:0\r\n
            slave_repl_offset:88619\r\n
            slave_priority:100\r\n
            slave_read_only:1\r\n
            connected_slaves:0\r\n
            master_replid:96e151af1ceabb08e578123751362e53dd8a9054\r\n
            master_replid2:0000000000000000000000000000000000000000\r\n
            master_repl_offset:88619\r\n
            second_repl_offset:-1\r\n
            repl_backlog_active:1\r\n
            repl_backlog_size:1048576\r\n
            repl_backlog_first_byte_offset:1\r\n
            repl_backlog_histlen:88619\r\n",
    "action":"GET",
    "pod_ip":"10.1.37.13"
}

$ curl -X GET 127.0.0.1:30003/get?key=key_1
{
    "key":"key_1",
    "value":"get key_1: value_1",
    "redis_replication":"
        # Replication\r\n
            role:slave\r\n
            master_host:10.152.183.182\r\n
            master_port:6379\r\n
            master_link_status:up\r\n
            master_last_io_seconds_ago:6\r\n
            master_sync_in_progress:0\r\n
            slave_repl_offset:88619\r\n
            slave_priority:100\r\n
            slave_read_only:1\r\n
            connected_slaves:0\r\n 
            master_replid:96e151af1ceabb08e578123751362e53dd8a9054\r\n
            master_replid2:0000000000000000000000000000000000000000\r\n
            master_repl_offset:88619\r\n
            second_repl_offset:-1\r\n
            repl_backlog_active:1\r\n
            repl_backlog_size:1048576\r\n
            repl_backlog_first_byte_offset:1\r\n
            repl_backlog_histlen:88619\r\n",
     "action":"GET",
    "pod_ip":"10.1.37.14"
}

$ curl -X GET 127.0.0.1:30003/get?key=key_1
{
    "key":"key_1",
    "value":"get key_1: value_1",
    "redis_replication":"
        # Replication\r\n
            role:slave\r\n
            master_host:10.152.183.182\r\n
            master_port:6379\r\n
            master_link_status:up\r\n
            master_last_io_seconds_ago:7\r\n
            master_sync_in_progress:0\r\n
            slave_repl_offset:88619\r\n
            slave_priority:100\r\n
            slave_read_only:1\r\n
            connected_slaves:0\r\n
            master_replid:96e151af1ceabb08e578123751362e53dd8a9054\r\n
            master_replid2:0000000000000000000000000000000000000000\r\n
            master_repl_offset:88619\r\n
            second_repl_offset:-1\r\n
            repl_backlog_active:1\r\n
            repl_backlog_size:1048576\r\n
            repl_backlog_first_byte_offset:1\r\n
            repl_backlog_histlen:88619\r\n",
    "action":"GET",
    "pod_ip":"10.1.37.15"
}
```

结果: 从 key-value-app http server 返回的内容可以看出,当执行 set 的时候,请求被发送到了 redis-master, 当执行 get 的时候,请求被发送
     到了 redis-slave, 并且因为 key-value-app 的副本数为 3 , 所以发送三次 get 请求分别请求到了不同的副本(可以通过`pod_id` 看出).  

*疑问*:   

上面的测试中,redis-salve 返回的 redis Replication 中, master host 均为 `10.152.183.182`,这一点不难理解,因为 redis-master 的 Service 的 CLUSTER_IP 就是 `10.152.183.182`:
```
$ kubectl get svc
    NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
    key-value-app        NodePort    10.152.183.61    <none>        8082:30003/TCP   16h
    kubernetes           ClusterIP   10.152.183.1     <none>        443/TCP          18h
    redis-master         ClusterIP   10.152.183.182   <none>        6379/TCP         17h
    redis-master-local   NodePort    10.152.183.228   <none>        6379:30001/TCP   17h
    redis-slave          NodePort    10.152.183.66    <none>        6379:30002/TCP   17h
```
但是 redis master  返回的 redis Replication 信息中,可以发现以两个 salve, ip 和 port 相同,均为 `10.1.37.1:6379`,这一点我现在还不理解,但可以确定的是 redis master 和 slave 的连接是没有问题的.



### 第九步: 清理 <a id="step-nine"></a>
完成本试验后,可以使用 `kubectl delete -f ...` 命令
```console
$ kubectl delete -f redis-master-deploy.yaml

$ kubectl delete -f redis-master-svc.yaml

$ kubectl delete -f redis-slave-deploy.yaml

$ kubectl delete -f redis-slave-svc.yaml

$ kubectl delete -f key-value-app-deploy.yaml

$ kubectl delete -f key-value-app-svc.yaml

```


### 其他
- 为每一个资源对象都新建一个 `yaml` 会使项目可读性变差,操作起来也比较繁琐,所以在最佳实践中推荐将一个应用的所有资源对象定义在一个 `yaml` 文件中.
- 在企业项目中, 拉取镜像时一定要执行镜像的版本, 这样更方便更新 