import { isArray, find, reduce } from 'lodash'
import User from '@/models/User'

export function defaultHeaders () {
  return {
    'content-type': 'application/vnd.api+json',
    'x-csrftoken': User.me().csrf_token
  }
}

export function recordNormalizer ({ id, type, attributes = {}, relationships }, included = [], depth = 4) {
  const include = find(included, { type, id })
  relationships = relationships || include?.relationships || {}
  const relationshipFields = reduce(relationships, (all, { data = null }, field) => {
    if (depth < 1 || data === null) {
      all[field] = null
    } else if (isArray(data)) {
      all[field] = data.map(relatedRecord => recordNormalizer(relatedRecord, included, depth - 1))
    } else {
      all[field] = recordNormalizer(data, included, depth - 1)
    }
    return all
  }, {})
  return { id, type, ...relationshipFields, ...attributes, ...include?.attributes }
}

export function responseNormalizer ({ data: { data = [], included = [] } }) {
  if (isArray(data)) {
    return data.map(record => {
      return recordNormalizer(record, included, 4)
    })
  }
  return recordNormalizer(data, included)
}
