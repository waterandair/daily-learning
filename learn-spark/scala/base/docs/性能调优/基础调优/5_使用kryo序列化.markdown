### 说明
默认情况下,Spark 内部是使用 java 的序列化机制,ObjectOutputStream/ObjectInputStream,对象输入输出流机制,来进行序列化
这种默认序列化机制的好处在于,处理起来比较方便,只需要在算子里使用的变量,必须是实现 Serializable 接口的,可序列化即可.
缺点在于,默认的序列化机制的效率不高,序列化的速度比较慢,序列化以后的数据,占用的内存空间相对还是比较大的

可以手动进行序列化格式的优化,Spark支持使用 Kryo 序列化机制,Kryo 序列化机制,比默认的java机制速度要快,序列化以后的数据要更小,
大概是java序列化机制的 1/10

### 启用序列化机制后,会生效的几个地方
1. 算子函数中使用的外部变量
2. 持久化 RDD 时进行序列化, StorageLevel.MEMORY_ONLY_SER
3. shuffle

### 设置 Kryo 序列化
#### 第一步: 在 SparkConf 中设置一个属性
```
SparkConf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
```
#### 第二步: 注册使用到的需要通过 Kryo 序列化的,一些自定义类 SparkConf.registerKryoClasses()
```
.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
.registerKryoClasses(new Class[]{CategorySortKey.class})
```


