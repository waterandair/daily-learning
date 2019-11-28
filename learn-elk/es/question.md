### 记录一些常见问题

#### 基础

##### 动态 mapping

#### 搜索
- 一般搜索会对返回的结果列表进行相关度评分,如果不需要频分,可以使用 constant_score 将 Query 转成 Filter,忽略 TF-IDF 计算,避免相关性算分的开销,且可以利用缓存
- 在 es 中搜索上下文有 query Context 和 filter Context, query Context 会计算相关性评分, Filter 不会,可以利用cache
-

##### 搜索类型
- 基于 term 的查找有:　Term Query / Range Query / Exists Query / Prefix Query /Wildcard Query；
- 基于全文的搜索有：　Match Query / Match Phrase Query / Query String Query；　搜索前会先对搜索字符串进行分词．
- 多字段,多条件的 bool query.
- 单字符串多字段查询 multi match
- Function Score Query, 在查询结束后,对每个匹配的文档进行一系列的重新算分,根据新生成的分数进行排序. 提供了多种函数,自定义脚本,完全控制算分
 
##### bool 查询
子查询的顺序可以是任意的,可以嵌套多个子查询.一个 bool 查询可以包括四种子句.  
- must 必须匹配,贡献评分
- should 选择性匹配,贡献评分
- must_not 必须不能匹配,属于 filter context 的查询,不计算评分
- filter 必须匹配,属于 filter context 的查询,不贡献评分

同一层级下的竞争字段,算分时具有相同的权重,可以通过嵌套 bool 查询, 改变算分.  

可以通过 boosting 控制字段在计算相关度评分时的权重: 
- boost > 1, 打分相关度相对提升
- 0 < boost < 1, 打分相关度相对降低
- boost < 0, 贡献负分

##### Disjunction Max Query(单个字段最高评分作为最终评分) 解决多字段评分竞争
多字段查询时,最终的相关度评分是各个字段相关度评分的总和,这样不利于找出最佳匹配的单个字段.  

可以使用 `dis_max`, 以最佳匹配字段的评分作为最终评分.  

使用了 `dis_max` 这种方式过于绝对,可以使用 `tie_breaker` 与其他字段的匹配评分相乘,最终将所有字段的匹配求和作为最终评分.  
tie_breaker 参数为 0 表示使用最佳匹配,为 1 表示所有字段同等重要.

##### multi match
三种类型: 
- 最佳字段(best_fields): 默认类型;最终评分来自最佳匹配字段.
- 多数字段(most_fields): 匹配到的字段越多越好.
- 混合字段(cross_fields): 在列出的字段中,匹配到越多的字段越好.比如检索地址信息,有 `country, city, street` 等字段,可以使用 `cross_fields` 的方式搜索,替代 copy_to 的方式 


##### suggester 搜索建议
四种类型: 
- Term: 词语搜索
- Phrase: 短语搜索
- Complete:　提供了自动完成的功能, 用户没输入一个词,就要发送一个请求去进行匹配,es 将 Analyze 的数据编码成 FST 和索引一起存放。FST 会被 ES 整个加载进内存,速度很快,但只能用于前缀搜索
- Context: Complete Suggester 的扩展.

每一种 suggester 都有三种模式:
- missing: 只有在索引搜索中没有找到结果,才会提供建议
- popular: 推荐出现频率高的词
- always: 无论是否搜到结果,都提供建议

##### 分布式搜索流程
- query 阶段: 用户向es发送查询请求, 接收到请求的 coordinating 节点将请求随机转发到半数的分片上.被选中的分片执行查询,进行排序.每个分片都会向 coordinating 节点返回 form+size 个排序后的分档ID
- fetch 阶段: coordinating 节点对 query 节点接收到的各个分片的 form+size 个排序好的文档ID进行重新排序. 然后以 multi get 的方式到对应分片上获取详细信息,然后返回给用户.

##### 搜索性能问题:
- 每个分片上需要查询的文档个数 = from + size
- coordinating 节点需要处理的文档个数 = number_of_shard * (from + size)

###### 解决深度分页问题
- 为了避免深度分页, es 默认限制 from + size < 10000
- 使用 search_after, 减少分片传给 coordinating 节点的文档数


##### 搜索相关性算分问题:
- 每个分片都只是基于自己分片上的数据,进行计算,这回导致计算偏离.特别是在文档数少,但分片数多的情况下.
- 数据量不大的时候,将主分片数设置为 1.当数据量足够大的时候,要保证文档均匀分布到各个分片上.

#### 聚合

##### Pipeline aggregations 

Pipeline 的分析结果会输出到原结果中,根据位置的不不同,分为两类

Sibling 结果和现有分析结果同级: Max,min,Avg & Sum Bucket,Stats,Extended Status Bucket,Percentiles Bucket
Parent - 结果内嵌到现有的聚合分析结果之中: Derivative (求导), Moving Function (滑动窗口), Cumultive Sum (累计求和)

##### 聚合的范围

ES 聚合分析的默认作用范围是 query 的查询结果集,可以通过指定以下方式改变范围: 

- filter(在aggs内): 只对当前的自聚合语句生效
- post_filter(与aggs同级): 对聚合分析后的文档进行过滤
- global: 无视一切约束,对全部文档进行聚合分析  

##### 聚合的排序
- 直接使用 `_count` 或 `_key` 进行排序
- 使用子聚合的结果进行排序

#### 处理关联关系
四种方式: 
- 对象类型: 直接把关联的对象以json对象的方式记录到一个字段上, 这种方式下,json对象中的字段不会被建立索引
- 嵌套对象: 与对象类型类似,但解决了对象类型不会被加入索引的问题.
- 父子关联关系: 分别将数据索引到父子两个文档,子文档可以独立更新.
- 应用端关联: - 

| - | Nested Object | Parent/Child |
| --- | --- | ---|
| 优点 | 文档存储在一起,读取性能高 | 父子文档可以独立更新 |
| 缺点 | 更新子文档,整个文档都会被更新 | 需要额外的内存维护关系,读取性能还差 |
| 适用场景 | 读多更新少 | 读少,子文档频繁更新 |

#### 重建索引
需要重建索引的情况: 
- 索引的 mapping 发生更改,比如字段类型改变,分词器改变和字典更新
- 索引的 setting 发生变化,比如主分片数发生更改
- 集群间做数据迁移

重建索引的方法;
- Update By Query: 在现有索引上重建
- Reindex: 在其他索引上重建



#### Ingest Pipeline 预处理
