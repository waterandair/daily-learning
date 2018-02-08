package sql.udf
import org.apache.spark.Aggregator
import org.apache.spark.sql.expressions.{Aggregator, MutableAggregationBuffer, UserDefinedAggregateFunction}
import org.apache.spark.sql.types._
import org.apache.spark.sql.{Encoder, Encoders, Row}

class MyAverage extends UserDefinedAggregateFunction {
  // data types of input arguments of this aggregate function
  override def inputSchema: StructType = {
    StructType(StructField("inputColumn", LongType, nullable = true) :: Nil)

  }

  // data types of values in the aggregation buffer
  override def bufferSchema: StructType = {
    StructType(StructField("sum", LongType)::StructField("count", LongType):: Nil)
  }

  // the data of return value
  override def dataType: DataType = DoubleType

  // whether this function always returns the same output on the identical input
  override def deterministic: Boolean = true

  /*
    Initializes the given aggregation buffer. The buffer itself is a 'Row' that in addition
    to standard methods likes retrieving a value at an index(e.g. get(), getBoolean()), provides
    the opportunity to update its values. Note that arrays and maps inside the buffer are still immutable
   */
  override def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer(0) = 0L
    buffer(1) = 0L
  }

  // updates the given aggregation buffer 'buffer' with new input data from 'input'
  override def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    if(!input.isNullAt(0)) {
      buffer(0) = buffer.getLong(0) + input.getLong(0)
      buffer(1) = buffer.getLong(1) + 1
    }
  }

  // merges two aggregation buffers and stores the updated buffer values back to 'buffer1'
  override def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    buffer1(0) = buffer1.getLong(0) + buffer2.getLong(0)
    buffer1(1) = buffer1.getLong(1) + buffer2.getLong(1)
  }

  // calculates the final result
  override def evaluate(buffer: Row): Double = {
    buffer.getLong(0).toDouble / buffer.getLong(1)
  }
}
