import scala.io.Source

object WordCount {
  def main(args: Array[String]): Unit = {
    val file = Source.fromFile("/usr/local/spark-2.2.1/README.md")
    var wordCount = scala.collection.mutable.Map[String, Int]()
    var words = file.getLines().flatMap(line => line.split(" ")).foreach(
      word => {
        if (wordCount.contains(word)) {
          wordCount(word) += 1
        } else {
          wordCount += (word -> 1)
        }
      }
    )

    wordCount.foreach(kv => printf("%s -> %d\n", kv._1, kv._2))
  }
}
