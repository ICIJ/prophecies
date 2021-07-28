import { Model } from '@vuex-orm/core'
import settings from '@/settings'

export default class Project extends Model {
  static entity = 'projects'

  static fields () {
    return {
      id: this.attr(null),
      name: this.string()
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/projects/`
  }
}
