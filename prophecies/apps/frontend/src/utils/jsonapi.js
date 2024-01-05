import { isArray, isPlainObject, find, mapValues, reduce } from 'lodash'
import User from '@/models/User'

const MAX_RELATIONSHIP_DEPTH = 10

export function defaultHeaders () {
  return {
    'content-type': 'application/vnd.api+json',
    'x-csrftoken': User.me().csrfToken
  }
}

class ResponseNormalizer {
  constructor ({ data }) {
    this.data = data.data
    this.included = data.included || []
  }

  findIncluded ({ type, id }) {
    return find(this.included, { type, id })
  }

  normalize () {
    if (isArray(this.data)) {
      return this.data.map(record => this.recordNormalizer(record))
    }
    return this.recordNormalizer(this.data)
  }

  recordNormalizer ({ id, type, attributes = {}, relationships } = {}, depth = MAX_RELATIONSHIP_DEPTH) {
    const included = this.findIncluded({ type, id })
    return {
      id,
      type,
      ...attributes,
      ...this.relationshipsNormalizer(relationships || included?.relationships, depth - 1),
      ...included?.attributes
    }
  }

  relationshipsNormalizer (relationships = {}, depth = MAX_RELATIONSHIP_DEPTH) {
    if (depth < 1) {
      return {}
    }
    const normalized = mapValues(relationships, r => this.relationshipNormalizer(r, depth - 1))
    return this.spreadRelationships(normalized)
  }

  spreadRelationships (normalizedRelationships) {
    return reduce(normalizedRelationships, (normalized, rel, field) => {
      if (isPlainObject(rel)) {
        normalized[`${field}Id`] = normalized[`${field}Id`] || rel.id
        normalized[`${field}Type`] = normalized[`${field}Type`] || rel.type
      }
      return normalized
    }, normalizedRelationships)
  }

  relationshipNormalizer ({ data }, depth = MAX_RELATIONSHIP_DEPTH) {
    if (isArray(data)) {
      return data.map(relatedRecord => this.recordNormalizer(relatedRecord, depth - 1))
    } else if (data !== null) {
      return this.recordNormalizer(data, depth - 1)
    }
    return null
  }

  static create (...args) {
    return new ResponseNormalizer(...args)
  }
}

export function responseNormalizer (response) {
  return ResponseNormalizer.create(response).normalize()
}
