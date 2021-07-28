import { Model } from '@vuex-orm/core'
import Choice from '@/models/Choice'

export default class ChoiceGroup extends Model {
  static entity = 'choiceGroups'

  static fields () {
    return {
      id: this.attr(null),
      name: this.string(),
      choices: this.hasMany(Choice, 'choice_group_id')
    }
  }
}
