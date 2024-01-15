import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'

export default class TaskTemplateSetting extends Model {
  static entity = 'TaskTemplateSetting'

  static fields () {
    return {
      id: this.attr()
    }
  }


  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-template-settings/`,
    dataTransformer: responseNormalizer
  }
}
