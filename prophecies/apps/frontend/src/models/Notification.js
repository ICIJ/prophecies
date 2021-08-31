import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import Action from '@/models/Action'
import User from '@/models/User'
import settings from '@/settings'

export default class Notification extends Model {
  static entity = 'Notification'

  static fields () {
    return {
      id: this.attr(null),
      recipientId: this.attr(null),
      recipient: this.belongsTo(User, 'recipientId'),
      actionId: this.attr(null),
      action: this.belongsTo(Action, 'actionId'),
      level: this.string(null),
      description: this.string(null),
      read: this.boolean(false),
      read_at: this.attr(null),
      created_at: this.attr(null)
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/notifications/`,
    dataTransformer: responseNormalizer
  }
}
