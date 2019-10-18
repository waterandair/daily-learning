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
