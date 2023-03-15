import { castArray, get, isArray, isString, noop, set, unset } from 'lodash'
import hotkeys from 'hotkeys-js'

const callbacks = {}

const parseValue = value => {
  if (!value) {
    return {}
  } else if (isString(value)) {
    return parseValue(JSON.parse(value.replace(/\'/gi, '"')))
  } else if (isArray(value) && value.length) {
    return { '': castArray(value).join('+') }
  }
  return value
}

class VNodeHotkey {
  constructor(el, binding, vnode) {
    this.el = el
    this.binding = binding
    this.vnode = vnode
  }  

  get value () {
    return parseValue(this.binding.value)
  }
  
  get valueEntries () {
    return Object.entries(this.value)
  }

  get valueKeys () {
    return Object.values(this.value)
  }

  get oldValue () {
    return parseValue(this.binding.oldValue)
  }

  get oldValueKeys () {
    return Object.values(this.oldValue)
  }

  get propagate () {
    return this.binding.modifiers.propagate === true
  }

  get uid () {
    return this.vnode.context._uid
  }

  get uidKey () {
    return `v-${this.uid}`
  }

  buildCallback (detail = null) {
    return e => {
      if (!this.propagate) {
        e.preventDefault()
        e.stopPropagation()
      }
      const event = new CustomEvent('shortkey', { detail })
      this.el.dispatchEvent(event)
    }
  }

  getCallback(keysAsStr, defaultValue = null) {
    return get(callbacks, [keysAsStr, this.uidKey], defaultValue)
  }

  getOrBuildCallback(keysAsStr, srcKey) {
    const callback = this.getCallback(keysAsStr) || this.buildCallback({ srcKey })
    set(callbacks, [keysAsStr, this.uidKey], callback)
    return callback
  }

  bind () {
    this.valueEntries.forEach(([srcKey, keysAsStr]) => {
      const callback = this.getOrBuildCallback(keysAsStr, srcKey)
      // Avoid binding hotkeys after the document is detroyed
      if (document) {
        hotkeys(keysAsStr, callback)
      }
      // Save the callback to be able to unbind it later
      set(callbacks, [keysAsStr, this.uidKey], callback)
    })
  }

  unbind () {
    this.valueKeys.forEach(this.unbindKeys.bind(this))
  }
  
  unbindOldValue () {
    this.oldValueKeys.forEach(this.unbindKeys.bind(this))
  }
  
  unbindKeys(keysAsStr) {
    const callback = this.getCallback(keysAsStr, noop)
    hotkeys.unbind(keysAsStr, callback)
    unset(callbacks, [keysAsStr, this.uidKey])
  }
  
  update () {
    this.unbindOldValue()
    this.bind()
  }

  static create (...args) {
    return new VNodeHotkey(...args)
  }
}

export default {
  bind(el, binding, vnode) {
    VNodeHotkey.create(el, binding, vnode).bind()
  },
  update(el, binding, vnode) {
    VNodeHotkey.create(el, binding, vnode).update()
  },
  unbind(el, binding, vnode) {
    VNodeHotkey.create(el, binding, vnode).unbind()
  }
}