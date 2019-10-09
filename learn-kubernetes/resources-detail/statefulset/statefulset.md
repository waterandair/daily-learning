# StatefulSet
- StatefulSet的核心功能,是对有状态的应用进行管理,就是通过某种方式记录这些应用的拓扑和存储状态，然后在 Pod 被重新创建时，能够为新 Pod 恢复这些状态。  
- StatefulSet 使用 Pod 模板创建 Pod 的时候，会对它们按照 Pod 的“名字+编号”的方式进行编号并固定了下来,在新建或者删除 Pod 的时候，StatefulSet 会严格按照这些Pod编号的顺序逐一进行这些操作。注意区别 ReplicaSet 中每个 Pod 中都是相同的,而 Stateful 管理的 Pod 都是不同的.
- StatefulSet 可以通过用 `spec.serviceName` 字段指定 Headless Service 的方式，为每个 Pod 创建一个固定并且稳定的 DNS 记录，来作为它的访问入口。  
- StatefulSet 可以通过用 `spec.volumeClaimTemplates` 字段为每个Pod分配并创建一个同样编号的 PVC, 这样 Kubernetes 就可以通过 Persistent Volume 机制为这个 PVC 绑定上对应的 PV，从而保证了每一个 Pod 都拥有一个独立的 Volume。重启后也不丢失.

StatefulSet 可以理解为一种特殊的 Deployment, 它的独特之处在于它管理的每个 Pod 都有一个固定的编号,通过这个编号,StatefulSet就使用Kubernetes里的两个标准功能：Headless Service和PV/PVC，实现了对Pod的拓扑状态和存储状态的维护。
