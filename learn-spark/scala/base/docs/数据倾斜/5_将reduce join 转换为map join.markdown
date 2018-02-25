### 普通的join
普通的 join,肯定是要 shuffle,肯定是 reduce join,先将所有相同的key,对应的values,汇聚到一个task中,然后再进行join

### reduce join 转换为 map join (使用 broadcast)
如果啷个 RDD 要进行 join, 其中一个 RDD 是比较小的,一个 RDD 是 100万 数据,一个 RDD 是 1万 数据(一个 RDD 是 1亿 数据,一个 RDD 是 100万 数据)

其中一个 RDD 必须是比较下的,broadcast 出去那个小 RDD 的数据以后,就会在每个 executor 的 block manager 中都驻留一份.要确保内存足够存放那
个小 RDD 中的数据

这种方式下,根本不会发生 shuffle 操作,肯定也不会发生数据倾斜;从根本上杜绝了 join 操作可能导致的数据倾斜问题

**对于 join 中有数据倾斜的情况,首先应该考虑到这种方法,前提是某个 RDD 比较小的情况下**

对于 join 这种操作,不光是考虑数据倾斜的问题,即使没有数据倾斜的问题,可完全可以优先考虑用 reduce join 转 map join 的技术,不要用普通的 join,
去通过 shuffle 进行数据的 join;完全可以通过简单的 map,使用 map join 的方式,牺牲一点内存资源,在可行的情况下,优先这么使用
### 不适用的情况
两个 RDD 都比较大, 将其中一个做成 broadcast,很可能导致内存不足