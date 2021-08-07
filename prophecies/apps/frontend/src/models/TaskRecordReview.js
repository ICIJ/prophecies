import { Model } from '@vuex-orm/core'
import { defaultHeaders, responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import Choice from '@/models/Choice'
import TaskRecord from '@/models/TaskRecord'
import User from '@/models/User'

export default class TaskRecordReview extends Model {
  static entity = 'task-record-reviews'

  static fields () {
    return {
      id: this.attr(null),
      url: this.string(),
      status: this.string(),
      note: this.string(),
      alternativeValue: this.string(null).nullable(),
      choice_id: this.attr(null),
      choice: this.belongsTo(Choice, 'choice_id'),
      taskRecord_id: this.attr(null),
      taskRecord: this.belongsTo(TaskRecord, 'taskRecord_id'),
      checker_id: this.attr(null),
      checker: this.belongsTo(User, 'checker_id'),
      history: this.hasMany(TaskRecordReview, 'taskRecord_id'),
      selected: this.boolean(false)
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-record-reviews/`,
    dataTransformer: responseNormalizer,
    actions: {
      find (id) {
        return this.get(`${id}/`)
      },
      save (id, { attributes = { }, relationships = { } } = { }) {
        const type = 'TaskRecordReview'
        const data = { type, id, attributes, relationships }
        return this.put(`${id}/`, { data }, { headers: defaultHeaders() })
      },
      selectChoice (id, { choice, ...attributes }) {
        return this.save(id, {
          attributes,
          relationships: {
            choice: {
              data: {
                type: 'Choice',
                id: choice.id
              }
            }
          }
        })
      }
    }
  }
}
