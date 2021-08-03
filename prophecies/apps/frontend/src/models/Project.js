import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'

export default class Project extends Model {
  static entity = 'projects'

  static fields () {
    return {
      id: this.number(null),
      name: this.string()
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/projects/`,
    dataTransformer: responseNormalizer
  }
}
