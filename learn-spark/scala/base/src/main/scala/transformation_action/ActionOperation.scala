package transformation_action

import org.apache.spark.{SparkConf, SparkContext}

object ActionOperation {
  def main(args: Array[String]): Unit = {
    //reduce()
    //collect()
    //count()
    //take()
    countByKey()

    //saveAsTextFile("hefs:xxx:9000/xxx/xxx") 可以把rdd直接存到hdfs上

  }

  def reduce(): Unit = {
    val conf = new SparkConf()
      .setAppName("reduce")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val numberArray = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val numbers = sc.parallelize(numberArray, 1)
    val sum = numbers.reduce(_ + _)

    println(sum)
  }

  /**
    * 将RDD中所有元素获取到本地客户端
    * 使用collect操作，将分布在远程集群上的doubleNumbers RDD的数据拉取到本地
    * 这种方式，一般不建议使用，因为如果rdd中的数据量比较大的话，比如超过1万条
    * 那么性能会比较差，因为要从远程走大量的网络传输，将数据获取到本地此外，
    * 除了性能差，还可能在rdd中数据量特别大的情况下，发生oom异常，内存溢出
    * 因此，通常，还是推荐使用foreach action操作，来对最终的rdd元素进行处理
    */
  def collect() {
    val conf = new SparkConf()
      .setAppName("collect")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val numberArray = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val numbers = sc.parallelize(numberArray, 1)
    val doubleNumbers = numbers.map { num => num * 2 }

    val doubleNumberArray = doubleNumbers.collect()

    for(num <- doubleNumberArray) {
      println(num)
    }
  }

  /**
    * 获取RDD元素总数
    */
  def count() {
    val conf = new SparkConf()
      .setAppName("count")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val numberArray = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val numbers = sc.parallelize(numberArray, 1)
    val count = numbers.count()

    println(count)
  }

  /**
    * 获取RDD中前n个元素
    */
  def take() {
    val conf = new SparkConf()
      .setAppName("take")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val numberArray = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val numbers = sc.parallelize(numberArray, 1)

    val top3Numbers = numbers.take(3)

    for(num <- top3Numbers) {
      println(num)
    }
  }

  def countByKey() {
    val conf = new SparkConf()
      .setAppName("countByKey")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val studentList = Array(Tuple2("class1", "leo"), Tuple2("class2", "jack"),
      Tuple2("class1", "tom"), Tuple2("class2", "jen"), Tuple2("class2", "marry"))
    val students = sc.parallelize(studentList, 1)
    val studentCounts = students.countByKey()

    println(studentCounts)  // Map(class1 -> 2, class2 -> 3)
  }

  def saveAsTextFile(){}
}
