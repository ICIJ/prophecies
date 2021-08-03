import { Model } from '@vuex-orm/core'
import ChoiceGroup from '@/models/ChoiceGroup'

export default class Choice extends Model {
  static entity = 'choices'

  static fields () {
    return {
      id: this.number(null),
      name: this.string(),
      value: this.string(),
      choice_group_id: this.attr(null),
      choice_group: this.belongsTo(ChoiceGroup, 'choice_group_id')
    }
  }
}
