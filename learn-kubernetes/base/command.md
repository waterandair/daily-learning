## 常用命令
### 执行容器的命令
```
# 执行 Pod 的 date 命令,默认使用 Pod 中的第一个容器
kubectl exec <pod-name> date

# 指定 Pod 中某个容器执行 date 命令
kubectl exec <pod-name> -c <container-name> date

# 通过 bash 获得 Pod 中某个容器的 TTY,相当于登录容器
kubectl exec -ti <pod-name> -c <container-name> /bin/bash
```



