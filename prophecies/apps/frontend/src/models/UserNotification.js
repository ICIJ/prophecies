import {Model} from '@vuex-orm/core'
import {defaultHeaders, responseNormalizer} from '@/utils/jsonapi'
import Action from '@/models/Action'
import Operation from '@/models/Operation'
import User from '@/models/User'
import settings from '@/settings'

export default class UserNotification extends Model {
  static entity = 'UserNotification'

  static fields() {
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
      markAsRead(id) {
        const attributes = {read: true}
        const type = 'UserNotification'
        const data = {attributes, id, type}
        return this.put(`${id}/`, {data}, {headers: defaultHeaders()})
      },
      bulkMarkAsRead(ids) {
        const headers = defaultHeaders()
        const operations = ids.map(id => ({id, method: 'update', payload: '1'}))
        const payloads = [
          {
            id: '1',
            value: {
              data: {
                type: 'UserNotification',
                attributes: {
                  read: true
                }
              }
            }
          }
        ]
        const data = {
          type: 'Operation',
          attributes: {operations, payloads}
        }
        return Operation.api().post('', {data}, {headers})
      }
    }
  }

  get i18n() {
    return this.action ? ['notification', this.action.i18n].join('.') : null
  }

  get link() {
    return this.action ? this.action.link : null
  }
}
