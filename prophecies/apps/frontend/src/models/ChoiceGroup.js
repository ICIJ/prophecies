import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import AlternativeValue from '@/models/AlternativeValue'
import Choice from '@/models/Choice'

export default class ChoiceGroup extends Model {
  static entity = 'ChoiceGroup'

  static fields () {
    return {
      id: this.attr(null),
      name: this.string(),
      alternativeValues: this.hasMany(AlternativeValue, 'choiceGroupId'),
      choices: this.hasMany(Choice, 'choiceGroupId')
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/choice-groups/`,
    dataTransformer: responseNormalizer,
    actions: {
      find (id, config = {}) {
        return this.get(`${id}/`, config)
      }
    }
  }
}
