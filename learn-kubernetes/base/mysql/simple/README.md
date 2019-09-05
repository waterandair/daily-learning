## 说明
这是学习 kubernetes 的第一个实例,在 kubernetes 中构建一个mysql 服务,并使其可以被 kubernetes 外的应用使用.  

### 步骤:
#### 建立副本控制器
```
kubectl apply -f mysql-rc.yaml
```
#### 建立mysql服务
将类型设置为 NodePort, 这样就通过 node(物理主机或虚拟机)的 IP 访问到mysql
```
kubectl apply -f mysql-svc.yaml
```