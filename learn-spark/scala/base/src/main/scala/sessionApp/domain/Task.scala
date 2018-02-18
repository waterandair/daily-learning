package sessionApp.domain


class Task extends Serializable {
  // 主键
  var taskid:Long = 0
  // 任务名称
  var taskName: String = null
  // 创建时间
  var createTime: String = null
  // 开始运行的时间
  var startTime: String = null
  // 结束运行的时间
  var finishTime: String = null
  // 任务类型
  var taskType: String = null
  // 任务状态
  var taskStatus: String = null
  // 使用 json 格式 封装用户提交任务对应的特殊的筛选参数
  var taskParam: String = null
}
