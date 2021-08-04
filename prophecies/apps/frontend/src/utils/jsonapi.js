import { isArray, find, reduce } from 'lodash'
import User from '@/models/User'

export function defaultHeaders () {
  return {
    'content-type': 'application/vnd.api+json',
    'x-csrftoken': User.me().csrf_token
  }
}

export function recordNormalizer ({ id, type, attributes = {}, relationships }, included = []) {
  const include = find(included, { type, id })
  relationships = relationships || include?.relationships || {}
  const relationshipFields = reduce(relationships, (all, { data = null }, field) => {
    if (isArray(data)) {
      all[field] = data.map(relatedRecord => recordNormalizer(relatedRecord, included))
    } else if (data === null) {
      all[field] = null
    } else {
      all[field] = recordNormalizer(data, included)
    }
    return all
  }, {})
  return { id, type, ...relationshipFields, ...attributes, ...include?.attributes }
}

export function responseNormalizer ({ data: { data = [], included = [] } }) {
  if (isArray(data)) {
    return data.map(record => {
      return recordNormalizer(record, included)
    })
  }
  return recordNormalizer(data, included)
}
