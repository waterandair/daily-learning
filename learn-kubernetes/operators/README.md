## 说明
Operator = CRD(Custom Resource Definition 自定义资源对象) + CustomController(自定义Controller)  

### CRD (Custom Resource Definition 自定义资源对象)
它的含义在允许用户在 kubernetes 集群中自定义一个与 Pod,Service,Deployment 等类似的资源对象.使用 CRD 定义了一个对象后,
就可以使用 `kubectl create,apply,patch,delete ...` 对它进行增删改查操作,所以可以把它理解为是定义了一种在 etcd 中存储的一种数据结构, 此时
kubernetes 尚且不能理解它的含义,无法对它进行调度. 要想让 kubernetes 理解自定义资源对象,就要为它编写 CustomController.  

#### CRD 资源对象详解

##### yaml 示例 
```
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: networks.samplecrd.k8s.io
spec:
  group: samplecrd.k8s.io
  version: v1alpha1
  names:
    kind: MyResource
    plural: myResources
  scope: Namespaced
```
##### 说明
在 Kubernetes 中，一个 API 对象在 Etcd 里的完整资源路径是由：Group（API组）、Version（API版本）和 Resource（API资源类型）三个部分组成的, 即 `/apis/{GROUP}/{API_VERSION}/RESOURCE`。  

常见的一些核心资源对象如 Pod, Node 等,它们的Group实际上是空的 `""`, 所以这类对象直接在 `/api/` 下,而对于非核心的则在 `/apis/` 下, 如 `/apis/batch/v1/jobs`  

在上面的示例中, `apiVersion` 字段中指定的 `apiextensions.k8s.io` 就是组名, `v1beta1` 就是 `CustomResourceDefinition` 对象的版本号. 而这个 CRD 中定义了
一个组名为 `samplecrd.k8s.io`, 版本为 `v1alpha1` 的 `MyResource` 资源对象, 并指定了它的复数形式为 `myResources`, `scope` 表示该对象是属于 `Namespace` 的,和 Pod 一样. 






