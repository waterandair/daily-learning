package appLog

class AccessSortKey(val first: Int, val second: Int) extends Ordered[AccessSortKey] with Serializable{
  override def compare(that: AccessSortKey): Int = {
    if (this.first - that.first != 0) {
      this.first - that.first
    } else {
      this.second - that.second
    }
  }
}