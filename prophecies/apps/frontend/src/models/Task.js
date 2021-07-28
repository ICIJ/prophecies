import { Model } from '@vuex-orm/core'
import settings from '@/settings'
import ChoiceGroup from '@/models/ChoiceGroup'
import Project from '@/models/Project'

export default class Task extends Model {
  static entity = 'tasks'

  static fields () {
    return {
      id: this.attr(null),
      name: this.string(),
      priority: this.number(null),
      project_id: this.attr(null),
      project: this.belongsTo(Project, 'project_id'),
      choice_group_id: this.attr(null),
      choice_group: this.belongsTo(ChoiceGroup, 'choice_group_id')
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/tasks/`
  }
}
