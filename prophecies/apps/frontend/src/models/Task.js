import { Model } from '@vuex-orm/core'
import settings from '@/settings'
import Project from '@/models/Project'

export default class Task extends Model {
  static entity = 'tasks'

  static fields () {
    return {
      id: this.attr(null),
      name: this.string(),
      project_id: this.attr(null),
      project: this.belongsTo(Project, 'project_id')
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/tasks/`
  }
}
