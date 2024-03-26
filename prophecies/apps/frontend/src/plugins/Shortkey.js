import { get, keys, noop, set, unset } from 'lodash'
import hotkeys from 'hotkeys-js'

export default class Shortkey {
  constructor() {
    this.callbacks = {}
    this.active = true
  }

  bind(keys, ...args) {
    // Deconstruct args to etheir get a scope with a callback of just a callback
    const [scope, callback] = args.length === 2 ? args : ['all', args.shift()]
    // Avoid binding hotkeys after the document is detroyed
    if (document) {
      // Ensure the key is not binded already
      this.unbind(keys)
      // Wrap the callback to activate/deactivate shortcut on demand
      const wrappedCallback = (event) => (this.active ? callback(event) : null)
      // Then bind it using Hotkeys
      hotkeys(keys, scope, wrappedCallback)
      // Save the callback to be able to unbind it later
      set(this.callbacks, [keys, scope], wrappedCallback)
    }
  }

  unbind(keys = null, scope = 'all') {
    if (!keys) {
      return this.unbindAll(scope)
    }
    hotkeys.unbind(keys, get(this.callbacks, [keys, scope], noop))
    unset(this.callbacks, [keys, scope])
  }

  unbindAll(scope = 'all') {
    keys(this.callbacks).forEach((keys) => {
      this.unbind(keys, scope)
    })
  }

  setScope(scope = 'all') {
    hotkeys.setScope(scope)
  }

  activate() {
    this.active = true
  }

  deactivate() {
    this.active = false
  }

  toggle(active = null) {
    this.active = active !== null ? active : !this.active
  }

  static install(Vue) {
    Vue.mixin({
      beforeCreate() {
        this.$shortkey = new Shortkey()
      },
      beforeDestroy() {
        this.$shortkey.unbind()
      }
    })
  }
}
