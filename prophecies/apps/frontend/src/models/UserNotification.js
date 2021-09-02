import { camelCase } from 'lodash'
import { Model } from '@vuex-orm/core'
import { defaultHeaders, responseNormalizer } from '@/utils/jsonapi'
import Action from '@/models/Action'
import User from '@/models/User'
import settings from '@/settings'

export default class UserNotification extends Model {
  static entity = 'UserNotification'

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
      readAt: this.attr(null),
      createdAt: this.attr(null)
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/user-notifications/`,
    dataTransformer: responseNormalizer,
    actions: {
      markAsRead (id) {
        const attributes = { read: true }
        const type = 'UserNotification'
        const data = { attributes, id, type }
        return this.put(`${id}/`, { data }, { headers: defaultHeaders() })
      }
    }
  }

  get i18n () {
    const { verb, targetType, actionObjectType } = this.action
    const path = ['notification', 'actions', verb, targetType, actionObjectType]
    return path.map(p => p ? camelCase(p) : '*').join('.')
  }
}
