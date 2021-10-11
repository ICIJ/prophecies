import { castArray, get, isArray, isString, noop, set, unset } from 'lodash'
import hotkeys from 'hotkeys-js'

const callbacks = {}

const parsedValue = value => {
  const json = isString(value) ? JSON.parse(value.replace(/\'/gi, '"')) : value
  if (isArray(json)) {
    return { '': castArray(json).join('+') }
  }
  return json
}

const parsedValueEntries = value => {
  return Object.entries(parsedValue(value))
}

const buildCallback = (el, propagate = false, detail = null) => {
  return e => {
    if (!propagate) {
      e.preventDefault()
    }
    const event = new CustomEvent('shortkey', { detail })
    el.dispatchEvent(event)
  }
}

export default {
  bind(el, binding, vnode) {
    const propagate = binding.modifiers.propagate === true
    const uid = vnode.context._uid
    parsedValueEntries(binding.value).forEach(([srcKey, keysAsStr]) => {
      const callback = buildCallback(el, propagate, { srcKey })
      hotkeys(keysAsStr, callback)
      // Save the callback to be able to unbind it later
      set(callbacks, [keysAsStr, uid], callback)
    })
  },
  unbind(el, { value }, vnode) {
    const uid = vnode.context._uid
    parsedValueEntries(value).forEach(([, keysAsStr]) => {
      const callback = get(callbacks, [keysAsStr, uid], noop)
      hotkeys.unbind(keysAsStr, callback)
      unset(callbacks, [keysAsStr, uid])
    })
  }
}