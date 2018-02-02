package transformation_action

import org.apache.spark.{SparkConf, SparkContext}

object TransformationOperation {
  def main(args: Array[String]): Unit = {
    //map()
    //filter()
    //flatMap()
    //groupByKey()
    //reduceByKey()
    //sortByKey()
    join()
  }

  /**
    * map 算子,任何类型的 RDD 都可以调用
    */
  def map(): Unit = {
    val conf = new SparkConf()
      .setAppName("map")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val numbers = Array(1, 2, 3, 4, 5)
    val numberRdd = sc.parallelize(numbers, 1)
    // 将集合中的每个元素都乘 2
    val multipleNumberRdd = numberRdd.map( _ *2)

    multipleNumberRdd.foreach(println)
  }

  /**
    * 对初始RDD执行filter算子，过滤出其中的偶数
    */
  def filter(): Unit = {
    val conf = new SparkConf()
      .setAppName("filter")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val numbers = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val numberRDD = sc.parallelize(numbers)
    val evenNumberRDD = numberRDD.filter(_ % 2 == 0)

    evenNumberRDD.foreach(println)
  }

  /**
    * 与map类似，但是对每个元素都可以返回一个或多个新元素。
    */
  def flatMap(): Unit = {
    val conf = new SparkConf()
      .setAppName("flatMap")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val lines = Array("hello you", "hello me", "hello world")
    val linesRDD= sc.parallelize(lines, 1)

    val words = linesRDD.flatMap(_.split(" "))

    words.foreach(println)
  }

  /**
    * Spark有些特殊的算子，也就是特殊的transformation操作。比如groupByKey、sortByKey、reduceByKey等，
    * 其实只是针对特殊的RDD的。即包含key-value对的RDD。而这种RDD中的元素，实际上是scala中的一种类型，
    * 即Tuple2，也就是包含两个值的Tuple。
    */

  /**
    * 根据key进行分组，每个key对应一个Iterable<value>
    */
  def groupByKey(): Unit = {
    val conf = new SparkConf()
      .setAppName("groupByKey")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val scoreList = Array(
      Tuple2("class1", 80),
      Tuple2("class2", 75),
      Tuple2("class1", 90),
      Tuple2("class2", 60)
    )
    val scoresRDD = sc.parallelize(scoreList)

    val groupedScoreRDD = scoresRDD.groupByKey()


    groupedScoreRDD.foreach(score => {
      println(score._1)
      score._2.foreach(score => println("--- " + score))
    })

  }

  /**
    * 对每个key对应的value进行reduce操作。
    */
  def reduceByKey(): Unit = {
    val conf = new SparkConf()
      .setAppName("reduceByKey")
        .setMaster("local")
    val sc = new SparkContext(conf)
    val scoreList = Array(
      Tuple2("class1", 80),
      Tuple2("class2", 75),
      Tuple2("class1", 90),
      Tuple2("class2", 60)
    )
    val scores = sc.parallelize(scoreList, 1)
    val totalScores = scores.reduceByKey(_ + _)

    totalScores.foreach(classScore => println(classScore._1 + ": " + classScore._2))
  }

  def sortByKey(): Unit = {
    val conf = new SparkConf()
      .setAppName("sortByKey")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val scoreList = Array(
      Tuple2(65, "leo"),
      Tuple2(50, "tom"),
      Tuple2(100, "marry"),
      Tuple2(85, "jack"))

    val scores = sc.parallelize(scoreList, 1)
    val sortedScores = scores.sortByKey(ascending = false)

    sortedScores.foreach(studentScore => println(studentScore._1 + ": " + studentScore._2))
  }


  /**
    * 对两个包含<key,value>对的RDD进行join操作，每个key join上的pair，都会传入自定义函数进行处理。
    */
  def join() {
    val conf = new SparkConf()
      .setAppName("join")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val studentList = Array(
      Tuple2(1, "leo"),
      Tuple2(2, "jack"),
      Tuple2(3, "tom"));

    val scoreList = Array(
      Tuple2(1, 100),
      Tuple2(2, 90),
      Tuple2(3, 60));

    val students = sc.parallelize(studentList);
    val scores = sc.parallelize(scoreList);

    val studentScores = students.join(scores)

    studentScores.foreach(studentScore => {
      println("student id: " + studentScore._1);
      println("student name: " + studentScore._2._1)
      println("student socre: " + studentScore._2._2)
      println("=======================================")
    })
  }

}
