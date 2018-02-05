package rdd

import org.apache.spark.{SparkConf, SparkContext}

/**
  * Spark 默认会把外部变量传输到每个 task 中.
  * Spark为此提供了两种共享变量，一种是Broadcast Variable（广播变量），另一种是Accumulator（累加变量）。
  * Broadcast Variable会将使用到的变量，仅仅为每个节点拷贝一份，更大的用处是优化性能，减少网络传输以及内存消耗。
  * Accumulator则可以让多个task共同操作一份变量，主要可以进行累加操作
  *
  * http://spark.apache.org/docs/latest/rdd-programming-guide.html#broadcast-variables
  */
object BroadcastVariables {
  def main(args: Array[String]): Unit = {
    //broadcast()
    accumulator()
  }

  /**
    * Broadcast Variable，是只读的。并且在每个节点上只会有一份副本，而不会为每个task都拷贝一份副本
    */
  def broadcast(): Unit = {
    val conf = new SparkConf()
      .setAppName("Broadcast")
      .setMaster("local")
    val sc = new SparkContext(conf)
    val factor = 3
    val factorBroadcast = sc.broadcast(factor)

    val arr = Array(1, 2, 3, 4, 5)
    val rdd = sc.parallelize(arr)
    val multipleRdd = rdd.map(_ * factorBroadcast.value)

    multipleRdd.foreach(println)
  }

  /**
    * Tasks running on a cluster can then add to it using the add method. However, they cannot read its value.
    * Only the driver program can read the accumulator’s value, using its value method
    */
  def accumulator(): Unit = {
    val conf = new SparkConf()
      .setAppName("Accumulator")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val sumAccumulator = sc.longAccumulator("My Accumulator")
    val array = Array(1, 2, 3, 4)
    val arrayRDD = array.foreach(_ => sumAccumulator.add(1))

    println(sumAccumulator.value)  //  4
  }
}
