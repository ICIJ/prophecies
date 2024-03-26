import { Model } from '@vuex-orm/core'

import settings from '@/settings'
import { responseNormalizer } from '@/utils/jsonapi'
import User from '@/models/User'
import Task from '@/models/Task'

export default class ActionAggregate extends Model {
  static entity = 'ActionAggregate'

  static fields() {
    return {
      id: this.attr(null),
      verb: this.string(),
      date: this.attr(null),
      taskId: this.attr(null),
      task: this.belongsTo(Task, 'taskId', 'id'),
      userId: this.attr(null),
      user: this.belongsTo(User, 'userId'),
      count: this.number()
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/action-aggregates/`,
    dataTransformer: responseNormalizer
  }
}
