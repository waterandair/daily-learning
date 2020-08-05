一个队列可以被多个消费者轮询的方式消费，而kafka一个分区只能被一个消费者消费
#### 交换器
相关术语：
- RoutingKey：路由键。生产者将消息发送给交换器的时候，一般会指定一个 RoutingKey， 用来指定这个消息的路由规则，RoutingKey 需要与交换器类型和 BindingKey 联合使用才能生效
- Binding: 绑定。将交换器与与队列关联起来。在绑定的时候指定一个 BindingKey 就可以知道将消息路由到那个队列；一个队列可以有多个BindingKey；BindingKey与交换器类型有关，比如 fanout 类型的交换器会无视 BindingKey
- 生产者将消息发送到交换器时，需要一个 RoutingKey， 当BindingKey 与 RoutingKey 相匹配时，消息就会被路由到对应的队列中。

类型：
- fanout：会把发送到给交换器的消息发送到所有与该交换器绑定的队列
- direct：把消息路由到 BindingKey 与 RoutingKey 完全匹配的队列
- topic: BindingKey 可以模糊匹配 Routing， `*`表示匹配一个单词，`#`表示匹配0个或多个单词；
- headers: 不依赖 BindingKey， 依赖消息自定义的 header，性能差没人用


#### 死信队列 DLX(Dead Letter Exchange)
当消息在一个队列中变成死信时，它能被发送一个死信队列中，进行后续操作。  
消息会变成死信的情况：  
- 消息被拒绝(Basic.Reject/Basic.Nack), 并且 requeue 参数为 false
- 消息过期
- 队列达到最大长度  


死信队列配合 TTL 还可以实现延迟队列。
#### 延迟队列
应用场景：  
- 订单支付超时，更新为异常订单。
- 定时电饭煲  

生产者为消息设定过期时间并指定死信队列，消费者监听死信队列

#### 优先队列
设置队列的 `x-max-priority` 参数。   

如果消费者消费速度大于生产速度，设置优先级并不会有什么作用。

#### 消息确认
- 消费者确认：
- 生产者确认：

#### 持久化
- 交换器持久化：如果交换器没有持久化，当 broker 重启后，交换器的元数据会丢失，但消息数据不会丢失，只是不能将消息发送到这个交换器了。
- 队列持久化：声明队列时， 将 `durable` 设置为 true。如果不持久化，broker 重启后，队列和数据都会丢失
- 消息持久化：设置deliveryMode为2

#### 其他
- rabbitmq broker 不会为消息设置过期时间，判断消息是否需要重新投递的唯一依据是消费者连接是否已经断开。这么设计的原因是，rabbitmq 允许消费者消费一条消息很久很久。


