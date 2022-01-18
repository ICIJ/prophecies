import { Model } from '@vuex-orm/core'
import { defaultHeaders, responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import User from '@/models/User'
import Task from '@/models/Task'

export default class TaskRecord extends Model {
  static entity = 'TaskRecord'

  static fields () {
    return {
      id: this.attr(null),
      url: this.string(),
      originalValue: this.string(),
      predictedValue: this.string(),
      link: this.string(),
      embeddableLink: this.string(),
      locked: this.boolean(),
      lockedById: this.attr(null),
      lockedBy: this.belongsTo(User, 'lockedById'),
      metadata: this.attr(null),
      rounds: this.number(),
      status: this.string(),
      taskId: this.attr(null),
      task: this.belongsTo(Task, 'taskId'),
      saved: this.boolean()
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-records/`,
    dataTransformer: responseNormalizer,
    actions: {
      save (id, { attributes = { }, relationships = { } } = { }) {
        const type = 'TaskRecord'
        const data = { type, id, attributes, relationships }
        return this.put(`${id}/`, { data }, { headers: defaultHeaders() })
      },
      lock (id) {
        const attributes = { locked: true }
        return this.save(id, { attributes })
      },
      unlock (id) {
        const attributes = { locked: false }
        return this.save(id, { attributes })
      },
      saveRecord (id) {
        const attributes = { saved: true }
        return this.save(id, { attributes })
      },
      unsaveRecord (id) {
        const attributes = { saved: false }
        return this.save(id, { attributes })
      }
    }
  }

  get lockedByMe () {
    return this.locked && this.lockedById === User.me().id
  }

  get lockedByOther () {
    return this.locked && this.lockedById !== User.me().id
  }
}
