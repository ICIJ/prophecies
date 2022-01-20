import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'

export default class User extends Model {
  // This is the name used as module name of the Vuex Store.
  static entity = 'User'
  static usernamePattern = /@([a-zA-Z0-9]{1,15}|project|task)/g

  static fields () {
    return {
      id: this.attr(null),
      username: this.attr(''),
      firstName: this.string(null).nullable(),
      lastName: this.string(null).nullable(),
      email: this.attr(''),
      emailMd5: this.attr(''),
      isStaff: this.boolean(false),
      isSuperuser: this.boolean(false),
      isMe: this.boolean(false),
      csrfToken: this.string(null).nullable(),
      lastLogin: this.attr(null).nullable()
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/users/`,
    dataTransformer: responseNormalizer,
    actions: {
      me () {
        return this.get('me/', {
          dataTransformer (response) {
            return { isMe: true, ...responseNormalizer(response) }
          }
        })
      }
    }
  }

  static me () {
    const [user = null] = this.query().where('isMe', true).get()
    return user
  }

  /**
   * Get first name of the user.
   */
  get displayName () {
    if (this.firstName) {
      return this.firstName
    }
    return this.username
  }

  /**
   * Get full name of the user.
   */
  get displayFullName () {
    if (!this.firstName || !this.lastName) {
      return this.username
    }
    return `${this.firstName} ${this.lastName}`
  }

  toString () {
    return this.displayName
  }
}
