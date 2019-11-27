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
- Function Score Query, 在查询结束后,对每个匹配的文档进行一系列的重新算分,根据新生成的分数进行排序. 提供了了多种函数,自定义脚本,完全控制算分
 
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

#### 聚合


#### 集群