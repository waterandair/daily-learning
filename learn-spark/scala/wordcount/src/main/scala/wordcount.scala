import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object Wordcount {
    def main(args: Array[String]) {
        val inputFile = "file:///usr/local/spark-2.2.1/README.md"
        val conf = new SparkConf().setAppName("WordCount").setMaster("local[4]")
        val sc = new SparkContext(conf)
        val textFile = sc.textFile(inputFile)
        val wordcount = textFile.flatMap(line => line.split(" ")).map(word => (word, 1)).reduceByKey((a, b) => a + b)
        wordcount.foreach(println)

    }
}
