package sql.udf

import org.apache.spark.sql.expressions.UserDefinedAggregateFunction
import org.apache.spark.sql.types.{StructType, DataType, StructField, StringType, IntegerType }
import org.apache.spark.sql.expressions.MutableAggregationBuffer
import org.apache.spark.sql.Row


class StringCount extends UserDefinedAggregateFunction {

  /**
    * inputSchema, 指的是,输入数据的类型
    * @return
    */
  override def inputSchema: StructType = {
    StructType(Array(
      StructField("str", StringType, true)
    ))
  }

  /**
    * bufferSchema 指的是,中间进行聚合时,所处理的数据的类型
    * @return
    */
  override def bufferSchema: StructType = {
    StructType(Array(
      StructField("count", IntegerType, true)
    ))
  }

  /**
    * 指的是, 函数返回的数据类型
    * @return
    */
  override def dataType: DataType = {
    IntegerType
  }

  override def deterministic: Boolean = {
    true
  }

  /**
    * 为每个分组的数据执行初始化操作
    * @param buffer
    */
  override def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer(0) = 0
  }

  /**
    * 指的是, 每个分组, 有新的值进来的时候,如何进行分组对应的聚合值的计算
    * @param buffer
    * @param input
    */
  override def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    buffer(0) = buffer.getAs[Int](0) + 1
  }

  /**
    * 由于 spark 是分布式的,所以一个分组的数据,可能会在不同的节点上进行局部聚合,就是 update
    * 但是,最后一个分组,在各个节点上的聚合值.要进行merge,也就是合并
    * @param buffer1
    * @param buffer2
    */
  override def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    buffer1(0) = buffer1.getAs[Int](0) + buffer2.getAs[Int](0)
  }

  /**
    * 最后,指的是,一个分组的聚合值,如何通过中间的缓存聚合值,最后返回一个最终的聚合值
    * @param buffer
    * @return
    */
  override def evaluate(buffer: Row): Any = {
    buffer.getAs[Int](0)
  }

}
