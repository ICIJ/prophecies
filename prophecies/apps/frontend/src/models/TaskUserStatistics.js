import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import User from '@/models/User'
import Task from './Task'

export default class TaskUserStatistics extends Model {
  static entity = 'TaskUserStatistics'

  static fields () {
    return {
      id: this.attr(null),
      taskId: this.attr(null),
      task: this.belongsTo(Task, 'taskId'),
      checkerId: this.attr(null),
      checker: this.belongsTo(User, 'checkerId'),
      round: this.number(0),
      doneCount: this.number(0),
      pendingCount: this.number(0),
      totalCount: this.number(0),
      progress: this.number(0)
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-user-statistics/`,
    dataTransformer: responseNormalizer,
    actions: {
      getByTask (taskId, config = {}) {
        const params = { ...config.params, 'filter[task]': taskId }
        return this.get('', { ...config, params })
      }
    }
  }
}
