import { Model } from '@vuex-orm/core'
import ChoiceGroup from '@/models/ChoiceGroup'

export default class Choice extends Model {
  static entity = 'choices'

  static fields () {
    return {
      id: this.attr(null),
      name: this.string(),
      value: this.string(),
      requireAlternativeValue: this.boolean(),
      shortkeys: this.string(null).nullable(),
      choiceGroupId: this.attr(null),
      choiceGroup: this.belongsTo(ChoiceGroup, 'choiceGroupId')
    }
  }
}
