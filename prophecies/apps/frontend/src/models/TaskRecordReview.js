import { Model } from '@vuex-orm/core'
import settings from '@/settings'
import TaskRecord from '@/models/TaskRecord'

export default class TaskRecordReview extends Model {
  static entity = 'task-record-reviews'

  static fields () {
    return {
      id: this.attr(null),
      url: this.string(),
      status: this.string(),
      note: this.string(),
      alternative_value: this.string(),
      choice: this.number(null),
      task_record_id: this.attr(null),
      task_record: this.belongsTo(TaskRecord, 'task_record_id')
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-record-reviews/`
  }
}
