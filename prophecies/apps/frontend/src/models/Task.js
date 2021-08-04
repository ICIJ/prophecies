import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import ChoiceGroup from '@/models/ChoiceGroup'
import Project from '@/models/Project'

export default class Task extends Model {
  static entity = 'tasks'

  static fields () {
    return {
      id: this.attr(null),
      url: this.string(),
      name: this.string(),
      description: this.string(),
      colors: this.attr(),
      priority: this.number(1),
      task_records_count: this.number(0),
      task_records_done_count: this.number(0),
      user_task_records_count: this.number(0),
      user_task_records_done_count: this.number(0),
      user_progress_by_round: this.attr(),
      user_progress: this.number(0),
      progress: this.number(0),
      progress_by_round: this.attr(),
      project_id: this.attr(null),
      project: this.belongsTo(Project, 'project_id'),
      rounds: this.number(1),
      choice_group_id: this.attr(null),
      choice_group: this.belongsTo(ChoiceGroup, 'choice_group_id')
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
