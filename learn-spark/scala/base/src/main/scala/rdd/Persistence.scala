package rdd

/**
  * 要持久化一个RDD，只要调用其cache()或者persist()方法即可。
  * 在该RDD第一次被计算出来时，就会直接缓存在每个节点中。而且Spark的持久化机制还是自动容错的，
  * 如果持久化的RDD的任何partition丢失了，那么Spark会自动通过其源RDD，使用transformation操作重新计算该partition。
  * cache()和persist()的区别在于，cache()是persist()的一种简化方式，cache()的底层就是调用的persist()的无参版本，
  * 同时就是调用persist(MEMORY_ONLY)，将数据持久化到内存中。如果需要从内存中清除缓存，那么可以使用unpersist()方法。
  * Spark自己也会在shuffle操作时，进行数据的持久化，比如写入磁盘，主要是为了在节点失败时，避免需要重新计算整个过程。
  *
  * 能不使用DISK相关的策略，就不用使用，有的时候，从磁盘读取数据，还不如重新计算一次。
  */
object Persistence {

}
