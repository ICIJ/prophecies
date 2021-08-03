import { Model } from '@vuex-orm/core'
import settings from '@/settings'

export default class User extends Model {
  // This is the name used as module name of the Vuex Store.
  static entity = 'users'

  static fields () {
    return {
      id: this.number(null),
      username: this.attr(''),
      first_name: this.string(null).nullable(),
      last_name: this.string(null).nullable(),
      email: this.attr(''),
      email_md5: this.attr(''),
      is_staff: this.boolean(false),
      is_me: this.boolean(false)
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/users/`,
    actions: {
      me () {
        return this.get('me/', {
          dataTransformer ({ data }) {
            return { is_me: true, ...data }
          }
        })
      }
    }
  }

  static me () {
    const [user = null] = this.query().where('is_me', true).get()
    return user
  }
}
