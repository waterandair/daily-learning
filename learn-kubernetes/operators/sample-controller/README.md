# 一步步实现 sample controller
[sample Controller](https://github.com/kubernetes/sample-controller) 是 kubernetes 演示 CRD 和 自定义控制器的一个案例.官方示例中没有
给出详细的实现步骤实现方法,本文将一步步的讲解如何实现这样一个自定义控制器去控制自己定义的 CRD

## 定义 CRD
[点击查看](crd/crd_foo.yaml)
```yaml
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: foos.samplecontroller.k8s.io
spec:
  group: samplecontroller.k8s.io
  version: v1alpha1
  names:
    kind: Foo
    plural: foos
  scope: Namespaced
```
上面的 yaml 文件中, 定义了一个分组为 `samplecontroller.k8s.io`, 版本为 `v1alpha1`, 名为 `Foo` 的 CRD(CustomResourceDefinition) 对象.
在这里只是声明了这种资源对象, 可以理解为在 apiServer 上定义了一个新的接口: `/apis/samplecontroller.k8s.io/v1alpha1/foo`, 这个接口实现的功能
就是对 `Foo` 这种资源对象进行增删改查.   

此时 kubernetes 只能对 Foo 对象的数据进行增删改查, 但无法理解 Foo 对象中定义的字段,无法对 Foo 对象进行编排.要想让 kubernetes 像理解编排 Pod 对象一样
理解 Foo 对象,就要完整自定义控制器(CustomController)  

## 定义 Foo 对象
[点击查看](crd/crd_foo.yaml)
```yaml
apiVersion: samplecontroller.k8s.io/v1alpha1
kind: Foo
metadata:
  name: example-foo
spec:
  deploymentName: example-foo
  replicas: 1
```
在上一小节,我们告诉了 kubernetes 集群我们要增加资源对象 `Foo`, kubernetes 会为我们新增一个用于对 `Foo` 对象进行增删改查的接口 `/apis/samplecontroller.k8s.io/v1alpha1/foo`,
这一小节,我们就来定义一个 `Foo` 对象具体的数据结构.  

在上面的 yaml 文件中,我们将 Foo 对象的 `apiVersion` 指定为 `samplecontroller.k8s.io/v1alpha1`, 将 Foo 对象的 `Kind` 定义为 `Foo`, 这与上一小节我们定义的 CRD 对象是一致.
此外我们为 Foo 定义了一个名字 `metadata.name = example-foo`, 这是每个资源对象都要定义的. 特殊之处在于,我们为 `Foo` 对象定义了两个自定义的字段 `spec.deploymentName` 和 `replicas`, 这两个字段的含义
是 kubernetes 暂时不能理解的,我们需要通过实现一个自定义的 Controller 来使 kubernetes 能够处理 Foo 对象的这两个字段

## 编写 sample-controller


