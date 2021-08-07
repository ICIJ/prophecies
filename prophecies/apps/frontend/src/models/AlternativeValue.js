import { Model } from '@vuex-orm/core'
import ChoiceGroup from '@/models/ChoiceGroup'

export default class AlternativeValue extends Model {
  static entity = 'alternative-values'

  static fields () {
    return {
      id: this.attr(null),
      name: this.string(),
      value: this.string(),
      choiceGroup_id: this.attr(null),
      choiceGroup: this.belongsTo(ChoiceGroup, 'choiceGroup_id')
    }
  }
}
