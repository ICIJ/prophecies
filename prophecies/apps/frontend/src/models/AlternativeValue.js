import { Model } from '@vuex-orm/core'
import ChoiceGroup from '@/models/ChoiceGroup'

export default class AlternativeValue extends Model {
  static entity = 'alternative-values'

  static fields () {
    return {
      id: this.attr(null),
      name: this.string(),
      value: this.string(),
      choice_group_id: this.attr(null),
      choice_group: this.belongsTo(ChoiceGroup, 'choice_group_id')
    }
  }
}
