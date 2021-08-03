import { isArray, find, reduce } from 'lodash'

export function recordNormalizer ({ id, type, attributes, relationships }, included = []) {
  const include = find(included, { type, id })
  relationships = relationships || include?.relationships || {}
  const relationshipFields = reduce(relationships, (all, { data }, field) => {
    if (isArray(data)) {
      all[field] = data.map(relatedRecord => recordNormalizer(relatedRecord, included))
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
