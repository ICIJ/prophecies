import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import ChoiceGroup from '@/models/ChoiceGroup'
import Project from '@/models/Project'
import TaskChecker from '@/models/TaskChecker'
import User from '@/models/User'

export default class Task extends Model {
  static entity = 'tasks'

  static fields () {
    return {
      id: this.attr(null),
      url: this.string(),
      name: this.string(),
      description: this.string(),
      checkers: this.belongsToMany(User, TaskChecker, 'checkerId', 'taskId'),
      colors: this.attr(),
      priority: this.number(1),
      taskRecordsCount: this.number(0),
      taskRecordsDoneCount: this.number(0),
      userTaskRecordsCount: this.number(0),
      userTaskRecordsDoneCount: this.number(0),
      userProgressByRound: this.attr(),
      userProgress: this.number(0),
      progress: this.number(0),
      progressByRound: this.attr(),
      projectId: this.attr(null),
      project: this.belongsTo(Project, 'projectId'),
      rounds: this.number(1),
      choiceGroupId: this.attr(null),
      choiceGroup: this.belongsTo(ChoiceGroup, 'choiceGroupId')
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/tasks/`,
    dataTransformer: responseNormalizer,
    actions: {
      find (id) {
        return this.get(`${id}/`)
      }
    }
  }
}
