#### 一个资源对象被创建的流程
- 向 APIServer 发起 POST 请求,提交用户编写的资源对象的yaml文件
- 根据资源对象的 `/{group}/{version}/{resource}` 找到它对应的 APIServer Handler
- APIServer 的 Handler 将 yaml 文件转换成一个 Super Version 的对象.他是该资源对象所有版本的字段全集
- APIServer 进行 admission(准入控制) 和 validation(验证对象里的字段是否合法) 操作.  
- APIServer 将验证过的API对象转换成用户最初提交的版本,进行序列化操作存入etcd 