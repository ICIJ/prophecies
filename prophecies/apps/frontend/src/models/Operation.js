import { Model } from '@vuex-orm/core'

import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'

export default class Operation extends Model {
  static entity = 'Operation'

  static fields() {
    return {}
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/operations/`,
    dataTransformer: responseNormalizer
  }
}
