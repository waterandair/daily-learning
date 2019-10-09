# DaemonSet
- DaemonSet 管理的 Pod 运行在 Kubernetes 集群里的每一个节点（Node）上；
- 每个节点上只有一个这样的 DaemonSet Pod 实例；
- 当有新的节点加入Kubernetes集群后，DaemonSet Pod 会自动地在新节点上被创建出来；而当旧节点被删除后，它上面的Pod也相应地会被回收掉。  
- 在创建每个Pod的时候，DaemonSet会自动给这个Pod加上一个 nodeAffinity，从而保证这个 Pod 只会在指定节点上启动。同时，它还会自动给这个 Pod 加上一个 Toleration ，从而忽略节点的unschedulable“污点”。  

## eg 
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd-elasticsearch
        image: k8s.gcr.io/fluentd-elasticsearch:1.20
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## nodeAffinity和Toleration
