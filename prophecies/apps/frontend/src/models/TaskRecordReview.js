import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import TaskRecord from '@/models/TaskRecord'
import Choice from '@/models/Choice'

export default class TaskRecordReview extends Model {
  static entity = 'task-record-reviews'

  static fields () {
    return {
      id: this.attr(null),
      url: this.string(),
      status: this.string(),
      note: this.string(),
      alternative_value: this.string(),
      choice_id: this.attr(null),
      choice: this.belongsTo(Choice, 'choice_id'),
      task_record_id: this.attr(null),
      task_record: this.belongsTo(TaskRecord, 'task_record_id')
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-record-reviews/`,
    dataTransformer: responseNormalizer
  }
}
