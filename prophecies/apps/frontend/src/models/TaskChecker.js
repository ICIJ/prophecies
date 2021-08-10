import { Model } from '@vuex-orm/core'
import Task from '@/models/Task'
import User from '@/models/User'

export default class TaskChecker extends Model {
  static entity = 'task-checkers'
  static primaryKey = ['checkerId', 'taskId']

  static fields () {
    return {
      id: this.attr(null),
      checkerId: this.attr(null),
      checker: this.belongsTo(User),
      taskId: this.attr(null),
      task: this.belongsTo(Task)
    }
  }
}
