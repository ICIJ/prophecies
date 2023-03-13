import {camelCase} from 'lodash'
import {Model} from '@vuex-orm/core'
import {responseNormalizer} from '@/utils/jsonapi'
import settings from '@/settings'

export default class Setting extends Model {
  // This is the name used as module name of the Vuex Store.
  static entity = 'Setting'
  static primaryKey = 'key'

  static fields() {
    return {
      key: this.string(null),
      value: this.attr('')
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/settings/`,
    dataTransformer: responseNormalizer
  }

  static allAsObject() {
    return this.all().reduce((all, {key, value}) => {
      // Setting key should be in camel case to match with Murmur config object
      all[camelCase(key)] = value
      return all
    }, {})
  }
}
