import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import Task from '@/models/Task'

export default class TaskTemplateSetting extends Model {
  static entity = 'TaskTemplateSetting'

  static fields () {
    return {
      id: this.attr(),
      task: this.belongsTo(Task, 'taskId'),
      taskId: this.attr(null),
    }
  }


  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-template-settings/`,
    dataTransformer: responseNormalizer
  }
}
