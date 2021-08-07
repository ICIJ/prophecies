import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import AlternativeValue from '@/models/AlternativeValue'
import Choice from '@/models/Choice'

export default class ChoiceGroup extends Model {
  static entity = 'choiceGroups'

  static fields () {
    return {
      id: this.attr(null),
      name: this.string(),
      alternativeValues: this.hasMany(AlternativeValue, 'choiceGroup_id'),
      choices: this.hasMany(Choice, 'choiceGroup_id')
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/choice-groups/`,
    dataTransformer: responseNormalizer,
    actions: {
      find (id) {
        return this.get(`${id}/`)
      }
    }
  }
}
