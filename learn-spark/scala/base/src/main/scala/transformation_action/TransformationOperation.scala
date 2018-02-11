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
    //join()
    //mapPartition()
    //sample()
    //union()
    //intersection()
    //distinct()
    //aggregateByKey()
    //cartesian()
    //coalesce()
    //repartition
    takeSample()
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
    * 其实RDD里是没有reduceByKey的，因此对RDD调用reduceByKey()方法的时候，会触发scala的隐式转换；
    * 此时就会在作用域内，寻找隐式转换，会在RDD中找到rddToPairRDDFunctions()隐式转换，然后将RDD转换为PairRDDFunctions。
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


  /**
    * mapPartition 类似 map, 不同之处在于 map 算子, 一次就处理一个 partition 中的一条数据
    * mapPartitions 算子, 一次处理一个 partition 中所有的数据
    *
    * 推荐使用的场景
    * 如果 RDD 数据量不是特别大,那么建议采用 mapPartitions 算子替代 map 算子,可以加快处理速度
    * 但是如果 RDD 的数据量特别大,比如说 10 亿, 不建议用 mapPartitions, 可能会内存溢出
    */
  def mapPartition(): Unit = {
    val conf = new SparkConf()
      .setAppName("mapPartition")
      .setMaster("local[2]")
    val sc = new SparkContext(conf)

    val studentNames = List("张三", "李四", "王二", "麻子")
    val studentNamesRDD = sc.parallelize(studentNames, 2)
    val studentScoreMap = Map(
      "张三" -> 278.5,
      "李四" -> 290.0,
      "王二" -> 301.0,
      "麻子" -> 205.0
    )

    val studentScoresRDD = studentNamesRDD.mapPartitions(iter =>  {
      var res = List[Double]()
      while (iter.hasNext) {
        val studentName = iter.next()
        val studentScore: Double = studentScoreMap.getOrElse(studentName, 0)
        res = res :+ studentScore
      }
      res.iterator
    })

    studentScoresRDD.foreach(println(_))
  }

  /**
    * sample
    * 可以使用指定的比例,比如说 0.1 或者 0.9, 从 RDD 中随机抽取 10% 或者 90%
    * 从 RDD 中随机抽取数据的功能
    * 推荐不要设置第三个参数, seed
    */
  def sample(): Unit ={
    val conf = new SparkConf()
      .setAppName("mapPartition")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val staffList = List("张三", "李四", "王二", "麻子", "赵六", "王五", "李大个", "王大妞", "小明", "小倩")
    val staffRDD = sc.parallelize(staffList)

    val luckStaffRDD = staffRDD.sample(withReplacement=false, 0.1)

    luckStaffRDD.foreach(println)
  }

  /**
    * 将两个 RDD 合并为一个 RDD
    */
  def union(): Unit = {
    val conf = new SparkConf()
      .setAppName("union")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val department1StaffList = List("张三", "李四", "王二", "麻子")
    val department1StaffRDD = sc.parallelize(department1StaffList)

    val department2StaffList = List("赵六", "王五", "小明", "小倩")
    val department2StaffRDD = sc.parallelize(department2StaffList)

    val departmentStaffRDD = department1StaffRDD.union(department2StaffRDD)

    for(staff <- departmentStaffRDD.collect()){
      println(staff)
    }
  }

  /**
    * 获取交集
    */
  def intersection(): Unit ={
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("intersection")
    val sc = new SparkContext(conf)

    val project1StaffList = List("张三", "李四", "王二", "麻子")
    val project1StaffRDD = sc.parallelize(project1StaffList)

    val project2StaffList = List("张三", "王五", "小明", "小倩")
    val project2StaffRDD = sc.parallelize(project2StaffList)

    val projectIntersectionRDD = project1StaffRDD.intersection(project2StaffRDD)

    for(name <- projectIntersectionRDD.collect()){
      println(name)
    }
  }

  /**
    * 对 RDD 中的数据去重
    * 使用场景:
    *   uv: user view 统计 每天每个用户可能对网站会点击多次
    *   此时,需要对用户进行去重,然后统计除每天有多少个用户访问了网站 而不是所有用户访问了网站多少次
    */
  def distinct(): Unit ={
    val conf = new SparkConf()
    .setMaster("local")
    .setAppName("intersection")
    val sc = new SparkContext(conf)

    val accessLogs = List(
      "user1 2016-01-01 23:58:42",
      "user1 2016-01-01 23:58:43",
      "user1 2016-01-01 23:58:44",
      "user2 2016-01-01 12:58:42",
      "user2 2016-01-01 12:58:46",
      "user3 2016-01-01 12:58:42",
      "user4 2016-01-01 12:58:42",
      "user5 2016-01-01 12:58:42",
      "user6 2016-01-01 12:58:42",
      "user6 2016-01-01 12:58:45"
    )
    val accessLogRDD = sc.parallelize(accessLogs)

    val useridsRDD = accessLogRDD.map(line => line.split(" ")(0))

    val distionctUseridsRDD = useridsRDD.distinct()
    val uv = distionctUseridsRDD.collect().size
    println("uv : " + uv)

  }

  /**
    * reduceByKey 可以认为是 aggregateByKey 的简化版
    * aggregateByKey 最重要的就是提供了一个函数与 Seq function
    * 就是说自己可以控制如何对每个 partition 中的数据进行先聚合,类似于 mapreduce中的 map-side combine
    * 然后才是对所有 partition 中的数据进行全局聚合
    *
    * 第一个参数是 每个key的初始值
    * 第二个是 seq 函数,表示如何进行本地聚合. 用来在一个partition中合并值的
    * 第三个是 combiner 函数,表示如何进行 shuffle reduce-side 的全局聚合, 用来在不同partition中合并值的
    */
  def aggregateByKey(): Unit ={
    val conf = new SparkConf()
      .setAppName("aggregateByKey")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val wordLines = List(
      "hello world you me",
      "hello hello you hello hello",
      "you you you",
      "me me"
    )
    val wordLinesRDD = sc.parallelize(wordLines, 4)

    val wordsRDD = wordLinesRDD.flatMap(_.split(" ")).map((_, 1))

    val wordCount = wordsRDD.aggregateByKey(0)(_ + _, _ + _)

    wordCount.foreach(println)
  }

  /**
    * 笛卡尔乘积
    * 比如说两个 RDD, 分别有 10 条数据, 用了 cartesian 算子以后,两个 RDD 的每一条数据都会和另外一个 RDD 的每一条数据执行一次 join
    * 最终组成一个 笛卡尔乘积
    * 案例
    *     比如说,现在5件衣服,5条裤子,分别属于两个 RDD
    *     就是说,需要对每件衣服和每条裤子做一次 join, 尝试进行服装搭配
    */
  def cartesian(): Unit = {
    val conf = new SparkConf()
      .setAppName("aggregateByKey")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val clothes = List("夹克", "T恤", "皮衣", "风衣")
    val clothesRDD = sc.parallelize(clothes)

    val trousers = List("皮裤", "运动裤", "牛仔裤", "休闲裤")
    val trousersRDD = sc.parallelize(trousers)

    val pairsRDD = clothesRDD.cartesian(trousersRDD)

    pairsRDD.foreach(println)

  }

  /**
    * coalesce 算子,功能是将 RDD 的 partition 缩减,减少
    * 将一定量的数据,压缩到更少的 partition 中去
    *
    * 使用场景:
    *         配合 filter 算子使用
    *         使用 filter 算子过滤掉很多数据以后,比如 30% 的数据,出现了很多 partition 中的数据不均匀的情况
    *         此时建议使用 coalesce 算子,压缩 rdd 的 partition 数量,从而让各个 partition 数量
    *         从而让各个 partition 中的数据都更加紧凑
    *
    */
  def coalesce(): Unit ={
    val conf = new SparkConf()
      .setAppName("aggregateByKey")
      .setMaster("local")
    val sc = new SparkContext(conf)

    val staffList = List("张三", "李四", "王二", "麻子", "赵六", "王五", "李大个", "王大妞", "小明", "小倩")
    val staffRDD = sc.parallelize(staffList, 6)

    val staffRDD2 = staffRDD.mapPartitionsWithIndex((index: Int, iter:Iterator[String])=>{
      var list = List[String]()

      while(iter.hasNext){
        val staff: String = iter.next()
        val str: String = "部门[" + (index + 1).toString + "], " + staff
        list  = list :+ str
      }
      list.iterator
    }, true)

   // staffRDD2.foreach(println)

    val staffRDD3 = staffRDD2.coalesce(3)
    val staffRDD4 = staffRDD3.mapPartitionsWithIndex((index: Int, iter:Iterator[String])=> {
      var list = List[String]()

      while(iter.hasNext){
        val staff = iter.next()
        val str = "部门[" + (index + 1).toString + "], " + staff
        list = list :+ str
      }
      list.iterator
    }, true)

    staffRDD4.foreach(println)
  }

  /**
    * 用于任意将 RDD 的 partition 增多或者减少
    * 与 coalesce 不同之处在于,coalesce 仅仅能将 rdd 的 partition 变少
    * 但是 repartition 可以将 RDD 的 partition 变多
    *
    * 使用场景:
    *         一个很经典的使用场景,使用 spark sql 从 hive 中查询数据时,
    *         spark sql 会根据hive 对应的hdfs 文件的 block 数量决定加载出来的数据 rdd 有多少个 partition
    *         这里的 partition 数量是无法设置的
    *         有时,可能它自动设置的 partition 数量过于少了,导致后面的算子的运算特别慢
    *         此时,就可以在 spark sql 加载 hive 数据到 rdd 以后
    *         立即使用 repartition 算子,将 rdd 的 partition 数量变多
    *
    *
    */
  def repartition(): Unit ={

  }

  /**
    * takeSample 算子
    * 与 sample 算子不同之处:
    *   1. takeSample 是 action 操作, sample 是 transformation 操作
    *   2. takeSample 不能抽取比例,只能设置抽取个数
    */
  def takeSample(): Unit ={
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName("takeSample")
    val sc = new SparkContext(conf)

    val staffList = List("张三", "李四", "王二", "麻子",
      "赵六", "王五", "李大个", "王大妞", "小明", "小倩")
    val staffRDD = sc.parallelize(staffList)

    val luckyStaffList = staffRDD.takeSample(withReplacement=false, 3)
    for(staff <- luckyStaffList){
      println(staff)
    }
  }

}
