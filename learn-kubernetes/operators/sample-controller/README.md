# 一步步实现 sample controller
[sample Controller](https://github.com/kubernetes/sample-controller) 是 kubernetes 演示 CRD 和 自定义控制器的一个案例.官方示例中没有
给出详细的实现步骤实现方法,本文将一步步的讲解如何实现这样一个自定义控制器去控制自己定义的 CRD

## 定义 CRD
[点击查看](crd/crd-foo.yaml)
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
[点击查看](crd/crd-foo.yaml)
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
### 目录结构简介
```
├── crd
│   ├── crd-foo.yaml                # CRD 定义
│   └── foo-example.yaml            # Foo 对象定义
|
├── main.go                         # 
├── pkg                             # ./pkg/apis/samplecontroller 文件夹根据组名命名 
    ├── apis
       └── samplecontroller
           ├── register.go          # 定义全局变量
           └── v1alpha1             
               ├── doc.go           # Golang的文档源文件
               ├── register.go      # 为客户端注册 Foo 类型,
               └── types.go         # 定义了对 Foo 对象的完整描述
...
```
### 编写代码
#### 定义全局变量 `./pkg/apis/samplecontroller/register.go`
```go
package samplecontroller

const (
	GroupName       = "samplecontroller.k8s.io"
	VersionV1alpha1 = "v1alpha1"
)
```
在 `/pkg/apis/samplecontroller/register.go` 中定义全局变量, 这里定义了 Foo 对象的组名和版本名

#### 定义 Foo 对象 `./pkg/apis/samplecontroller/v1alpha1/types.go`
```go
package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// +genclient
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// Foo is a specification for a Foo resource
type Foo struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   FooSpec   `json:"spec"`
	Status FooStatus `json:"status"`
}

// FooSpec is the spec for a Foo resource
type FooSpec struct {
	DeploymentName string `json:"deploymentName"`
	Replicas       *int32 `json:"replicas"`
}

// FooStatus is the status for a Foo resource
type FooStatus struct {
	AvailableReplicas int32 `json:"availableReplicas"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// FooList is a list of Foo resources
type FooList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata"`

	Items []Foo `json:"items"`
}

```
在注释中有关于代码的详细说明,在这里详细说明一下一些为了使用 kubernetes 生成代码工具而写的特定的形如`+<tag_name>[=value]`格式的注释.  

##### 为代码生成工具而写的特定的注释 [扩展阅读](https://blog.openshift.com/kubernetes-deep-dive-code-generation-customresources/)
###### // +genclient`
为 Foo 对象生成对应的 Client 代码

##### // +genclient:noStatus
为 Foo 对象生成的 Client 会自动带上 UpdateStatus方法.   
如果 Foo 对象没有 Status, 需要加上这个注释.

###### // +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object
在生成 DeepCopy 的时候，实现 Kubernetes 提供的 runtime.Object   接口。
否则，在某些版本的 Kubernetes 里，这个自定义对象类型会出现编译错误。这是一个固定的操作，记住即可。

#### 编写文档源文件 `./pkg/apis/samplecontroller/v1alpha1/doc.go`
```go
// +k8s:deepcopy-gen=package
// +groupName=samplecontroller.k8s.io

// Package v1alpha1 是 Foo 对象的 v1alpha1 版本
package v1alpha1
```
##### 为代码生成工具而写的特定的注释

###### // +k8s:deepcopy-gen=package
为整个 v1alpha1 包里的所有类型定义自动生成 DeepCopy 方法

###### // +groupName=samplecontroller.k8s.io

定义了 v1alpha1 包对应的 API 组的名字

#### 编写 Foo 的注册函数 `./pkg/apis/samplecontroller/v1alpha1/register.go`
```go
package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"

	"github.com/waterandair/daily-learning/learn-kubernetes/operators/sample-controller/pkg/apis/samplecontroller"
)

// SchemeGroupVersion 用于注册 Foo 资源对象的组和版本名
var SchemeGroupVersion = schema.GroupVersion{
	Group:   samplecontroller.GroupName,
	Version: samplecontroller.VersionV1alpha1,
}

// Kind 接收一个字符串类型的 kind, 将其进行转换返回一个标准的 Kind 类型
func Kind(kind string) schema.GroupKind {
	return SchemeGroupVersion.WithKind(kind).GroupKind()
}

// Resource 接受一个字符串类型的 resource, 将其进行转换一个标准的 Resource 类型
func Resource(resource string) schema.GroupResource {
	return SchemeGroupVersion.WithResource(resource).GroupResource()
}

var (
	// SchemeBuilder 初始化Scheme建造者
	SchemeBuilder = runtime.NewSchemeBuilder(addKnownTypes)
	// AddToScheme 是将 Foo 的组和版本注册到 API 的全局函数
	AddToScheme = SchemeBuilder.AddToScheme
)

// addKnownTypes 将自定义的 Foo 和 FooList 类型添加给 Scheme
func addKnownTypes(scheme *runtime.Scheme) error {
	scheme.AddKnownTypes(SchemeGroupVersion,
		&Foo{},
		&FooList{},
	)

	metav1.AddToGroupVersion(scheme, SchemeGroupVersion)
	return nil
}
```

#### 使用 `k8s.io/code-generator` 工具生成代码

```console
# 代码生成的工作目录，也就项目路径
$ ROOT_PACKAGE="github.com/waterandair/daily-learning/learn-kubernetes/operators/sample-controller"
# API Group
$ CUSTOM_RESOURCE_NAME="samplecontroller"
# API Version
$ CUSTOM_RESOURCE_VERSION="v1alpha1"

# 安装k8s.io/code-generator
$ go get -u k8s.io/code-generator
$ cd $GOPATH/src/k8s.io/code-generator

# 执行代码自动生成，其中pkg/client是生成目标目录，pkg/apis是类型定义目录
$ $GOPATH/src/k8s.io/code-generator/generate-groups.sh all "$ROOT_PACKAGE/pkg/client" "$ROOT_PACKAGE/pkg/apis" "$CUSTOM_RESOURCE_NAME:$CUSTOM_RESOURCE_VERSION"
```

注意: 本项目使用 go mod 管理依赖,要确保项目根目录下的 go.mod 文件中包含需要的包. 比如在本实例中, go.mod 在 `github.com/waterandair/daily-learning/` 目录下

##### 说明





