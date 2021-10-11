import { castArray, get, isArray, isString, noop, set, unset } from 'lodash'
import hotkeys from 'hotkeys-js'

const callbacks = {}

const parseValue = value => {
  if (!value) {
    return []
  } else if (isString(value)) {
    const json = JSON.parse(value.replace(/\'/gi, '"'))
    if (isArray(json)) {
      return { '': castArray(json).join('+') }
    }
    return json
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

  get oldValue () {
    return parseValue(this.binding.oldValue)
  }

  get oldValueEntries () {
    return Object.entries(this.oldValue)
  }

  get propagate () {
    return this.binding.modifiers.propagate === true
  }

  get uid () {
    return this.vnode.context._uid
  }

  buildCallback (detail = null) {
    return e => {
      if (!this.propagate) {
        e.preventDefault()
      }
      const event = new CustomEvent('shortkey', { detail })
      this.el.dispatchEvent(event)
    }
  }

  getCallback(keysAsStr, defaultValue = null) {
    return get(callbacks, [keysAsStr, this.uid], defaultValue)
  }

  getOrBuildCallback(srcKey, keysAsStr) {
    const callback = this.getCallback(keysAsStr) || this.buildCallback({ srcKey })
    set(callbacks, [keysAsStr, this.uid], callback)
    return callback
  }

  bind () {
    this.valueEntries.forEach(([srcKey, keysAsStr]) => {
      const callback = this.getOrBuildCallback(srcKey, keysAsStr)
      hotkeys(keysAsStr, callback)
      // Save the callback to be able to unbind it later
      set(callbacks, [keysAsStr, this.uid], callback)
    })
  }

  unbind () {
    this.valueEntries.forEach(([, keysAsStr]) => this.unbindKeys(keysAsStr))
  }

  unbindOldValue () {
    this.oldValueEntries.forEach(([, keysAsStr]) => this.unbindKeys(keysAsStr))
  }

  unbindKeys(keysAsStr) {
    const callback = this.getCallback(keysAsStr, noop)
    hotkeys.unbind(keysAsStr, callback)
    unset(callbacks, [keysAsStr, this.uid])
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