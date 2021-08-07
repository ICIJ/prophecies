import { isArray, find, mapValues } from 'lodash'
import User from '@/models/User'

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

  recordNormalizer ({ id, type, attributes = {}, relationships }, depth = 4) {
    const included = this.findIncluded({ type, id })
    return {
      id,
      type,
      ...attributes,
      ...this.relationshipsNormalizer(relationships || included?.relationships),
      ...included?.attributes
    }
  }

  relationshipsNormalizer (relationships = {}, depth = 4) {
    if (depth < 1) {
      return {}
    }
    return mapValues(relationships, r => this.relationshipNormalizer(r, depth))
  }

  relationshipNormalizer ({ data }, depth = 4) {
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
