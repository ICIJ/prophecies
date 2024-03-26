import { Model } from '@vuex-orm/core'

import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import Task from '@/models/Task'
import TaskRecord from '@/models/TaskRecord'

export default class TaskRecordMedia extends Model {
  static entity = 'TaskRecordMedia'

  static fields() {
    return {
      id: this.attr(null),
      mediaType: this.string(),
      mimeType: this.string(),
      file: this.string(),
      task: this.belongsTo(Task, 'taskId'),
      taskId: this.attr(null),
      taskRecord: this.belongsTo(TaskRecord, 'taskRecordId'),
      taskRecordId: this.attr(null),
      uid: this.string()
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-record-medias/`,
    dataTransformer: responseNormalizer,
    actions: {
      find(id, config = {}) {
        return this.get(`${id}/`, config)
      }
    }
  }
}
