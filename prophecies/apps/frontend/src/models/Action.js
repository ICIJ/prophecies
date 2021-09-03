import { camelCase, get, template } from 'lodash'
import { Model } from '@vuex-orm/core'
import { responseNormalizer } from '@/utils/jsonapi'
import TaskRecord from '@/models/TaskRecord'
import User from '@/models/User'
import settings from '@/settings'

export default class Action extends Model {
  static entity = 'Action'
  static links = {
    mentioned: {
      user: {
        tip: '#/tips',
        taskRecordReview: '#/task-record-reviews/{{ actionObject.taskId }}/{{ actionObject.id }}?highlightNote=true'
      }
    }
  }

  static fields () {
    return {
      id: this.attr(null),
      actorId: this.attr(null),
      actor: this.belongsTo(User, 'actorId'),
      verb: this.string(),
      targetId: this.attr(null),
      targetType: this.attr(null),
      target: this.morphTo('targetId', 'targetType'),
      actionObjectId: this.attr(null),
      actionObjectType: this.attr(null),
      actionObject: this.morphTo('actionObjectId', 'actionObjectType'),
      data: this.attr(() => {}),
      timestamp: this.attr(null)
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/actions/`,
    dataTransformer: responseNormalizer,
    actions: {
      forTaskRecord (id) {
        const { apiConfig } = TaskRecord
        const params = { 'page[size]': 50 }
        return this.get(`${id}/relationships/actions/`, { ...apiConfig, params })
      }
    }
  }

  get i18n () {
    const path = ['actions', this.verb, this.targetType, this.actionObjectType]
    return path.map(p => p ? camelCase(p) : '*').join('.')
  }

  get link () {
    const interpolate = settings.templateInterpolate
    const compiled = template(this.linkTemplate, { interpolate })
    return compiled(this)
  }

  get linkTemplate () {
    const path = [this.verb, this.targetType, this.actionObjectType]
    const key = path.map(p => p ? camelCase(p) : '*').join('.')
    return get(Action.links, key, null)
  }
}
