import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.log4j.{Level, Logger}

object WordCount {
  def main(args: Array[String]) = {
    // 屏蔽日志
    Logger.getLogger("org.apache.spark").setLevel(Level.WARN)
    Logger.getLogger("org.eclipse.jetty.server").setLevel(Level.OFF)

    val inputFile = "file:///usr/local/spark-2.2.1/README.md"
    val conf = new SparkConf().setAppName("WordCount").setMaster("local[4]")
    val sc = new SparkContext(conf)
    val textFile = sc.textFile(inputFile)
    val wordcount = textFile.flatMap(line => line.split(" ")).map(word => (word, 1)).reduceByKey((a, b) => a + b)
    wordcount.foreach(println)
  }
}
