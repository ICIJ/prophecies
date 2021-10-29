import { Model } from '@vuex-orm/core'
import { defaultHeaders, responseNormalizer } from '@/utils/jsonapi'
import settings from '@/settings'
import Choice from '@/models/Choice'
import Operation from '@/models/Operation'
import Task from '@/models/Task'
import TaskRecord from '@/models/TaskRecord'
import User from '@/models/User'

export default class TaskRecordReview extends Model {
  static entity = 'TaskRecordReview'

  static fields () {
    return {
      id: this.attr(null),
      url: this.string(),
      status: this.string(),
      note: this.string(null).nullable(),
      noteCreatedAt: this.attr(null).nullable(),
      noteUpdatedAt: this.attr(null).nullable(),
      alternativeValue: this.string(null).nullable(),
      choiceId: this.attr(null),
      choice: this.belongsTo(Choice, 'choiceId'),
      taskId: this.attr(null),
      task: this.belongsTo(Task, 'taskId'),
      taskRecordId: this.attr(null),
      taskRecord: this.belongsTo(TaskRecord, 'taskRecordId'),
      checkerId: this.attr(null),
      checker: this.belongsTo(User, 'checkerId'),
      history: this.hasMany(TaskRecordReview, 'taskRecordId'),
      selected: this.boolean(false)
    }
  }

  static apiConfig = {
    baseURL: `${settings.apiUrl}/task-record-reviews/`,
    dataTransformer: responseNormalizer,
    actions: {
      find (id, config = {}) {
        return this.get(`${id}/`, config)
      },
      search (query, config = {}) {
        const params = { ...config.params, 'filter[search]': query }
        return this.get('', { ...config, params })
      },
      save (id, { attributes = { }, relationships = { } } = { }) {
        const type = 'TaskRecordReview'
        const data = { type, id, attributes, relationships }
        return this.put(`${id}/`, { data }, { headers: defaultHeaders() })
      },
      bulkSelectChoice (ids, { choice, ...attributes }) {
        const headers = defaultHeaders()
        const operations = ids.map(id => ({ id, method: 'update', payload: '1' }))
        const payloads = [
          {
            id: '1',
            value: {
              data: {
                type: 'TaskRecordReview',
                attributes,
                relationships: {
                  choice: {
                    data: { type: 'Choice', id: choice.id }
                  }
                }
              }
            }
          }
        ]
        const data = {
          type: 'Operation',
          attributes: { operations, payloads }
        }
        return Operation.api().post('', { data }, { headers })
      },
      cancelChoice (id, { ...attributes }) {
        return this.save(id, {
          attributes,
          relationships: {
            choice: {
              data: null
            }
          }
        })
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

  get noteWithMentions () {
    return String(this.note).replace(User.usernamePattern, (match, p1) => {
      if (User.me() && p1 === User.me().username) {
        return `<span class="mention mention--is-me">${match}</span>`
      }
      return `<span class="mention">${match}</span>`
    })
  }

  get editable () {
    return this.checkerId === User.me()?.id
  }

  get locked () {
    const taskLocked = this.taskId && !Task.find(this.taskId)?.open
    const taskRecordLocked = this.taskRecordId && TaskRecord.find(this.taskRecordId)?.locked
    return !!(taskLocked || taskRecordLocked)
  }
}
