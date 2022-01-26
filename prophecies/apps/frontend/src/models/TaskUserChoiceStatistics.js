import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import Choice from '@/models/Choice'
import User from '@/models/User'
import Task from '@/models/Task'

export default class TaskUserChoiceStatistics extends Model {
  static entity = 'TaskUserChoiceStatistics'

  static fields () {
    return {
      id: this.attr(null),
      taskId: this.attr(null),
      task: this.belongsTo(Task, 'taskId'),
      checkerId: this.attr(null),
      checker: this.belongsTo(User, 'checkerId'),
      round: this.number(0),
      choiceId: this.attr(null),
      choice: this.belongsTo(Choice, 'choiceId'),
      count: this.number(0)
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-user-choice-statistics/`,
    dataTransformer: responseNormalizer
  }
}
