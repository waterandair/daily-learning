package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// +genclient
// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// Foo 定义了 Foo 资源对象
type Foo struct {
	// 标准的 kubernetes 资源对象都会包含 metav1.TypeMeta 和 metav1.ObjectMeta
	// metav1.TypeMeta 资源对象的元数据,比如 apiVersion 和 kind
	metav1.TypeMeta `json:",inline"`
	// metav1.ObjectMeta 一些特定的元数据,比如 name, namespace, labels 等等
	metav1.ObjectMeta `json:"metadata,omitempty"`

	// Spec 描述 Foo 对象自定义的字段
	Spec FooSpec `json:"spec"`
	// Status 描述 Foo 对象的状态
	Status FooStatus `json:"status"`
}

// FooSpec 定义了 Foo 对象的 spec 字段
type FooSpec struct {
	DeploymentName string `json:"deploymentName"`
	Replicas       *int32 `json:"replicas"`
}

// FooStatus 定义了 Foo 对象的状态
type FooStatus struct {
	AvailableReplicas int32 `json:"availableReplicas"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// FooList 定义了 Foo 对象的 list 形式, 用来描述一组 Foo 对象应该包含那些字段,在 kubernetes 中获取某种类型 T 的List()方法,返回的都是 List 类型,而不是 T 类型的数组
type FooList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata"`

	Items []Foo `json:"items"`
}
