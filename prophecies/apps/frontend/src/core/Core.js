// BootstrapVue recommends using this
import 'mutationobserver-shim'

import compose from 'lodash/fp/compose'
import Murmur from '@icij/murmur'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'
import VueI18n from 'vue-i18n'
import VueRouter from 'vue-router'
import VueScrollTo from 'vue-scrollto'
import VueWait from 'vue-wait'

import LocaleMixin from './LocaleMixin'

import Setting from '@/models/Setting'
import User from '@/models/User'
import router from '@/router'
import guards from '@/router/guards'
import store from '@/store'
import messages from '@/messages/en'
import settings from '@/settings'
import * as icons from '@/utils/icons'
import App from '@/views/App'
import vShortkey from '@/directives/shortkey'
import Shortkey from '@/plugins/Shortkey'

class Base {}
const Behaviors = compose(LocaleMixin)(Base)

/**
  @class
  @classdesc Class representing the core application.
  @mixes LocaleMixin
  @typicalname prophecies
*/
class Core extends Behaviors {
  /**
   * Create an application
   * @param {Object} LocalVue - The Vue class to instantiate the application with.
   */
  constructor(LocalVue = Vue) {
    super(LocalVue)
    this.LocalVue = LocalVue
    // Disable production tip when not in production
    this.LocalVue.config.productionTip = process.env.NODE_ENV === 'development'
    // All icon must be added to the local vue
    this.registerIcons()
    // Setup deferred state
    this.defer()
  }

  /**
   * Register all icons components
   * @returns {Array} icons components
   */
  registerIcons() {
    Object.values(icons).forEach(({ name, ...icon }) => {
      if (name) {
        this.LocalVue.component(name, icon)
      }
    })
  }

  /**
   * Add a Vue plugin to the instance's LocalVue
   * @param {Object} Plugin - The actual Vue plugin class
   * @param {Object} options - Option to pass to the plugin
   * @returns {Core} the current instance of Core
   */
  use(Plugin, options) {
    this.LocalVue.use(Plugin, options)
    return this
  }

  /**
   * Configure all default Vue plugins for this application
   * @returns {Core} the current instance of Core
   */
  useAll() {
    this.useI18n()
    this.useBootstrapVue()
    this.useCommons()
    this.useRouter()
    this.useWait()
    this.useCore()
    return this
  }

  /**
   * Configure vue-i18n plugin
   * @returns {Core} the current instance of Core
   */
  useI18n() {
    this.use(VueI18n)
    this.i18n = new VueI18n({
      locale: settings.defaultLocale,
      fallbackLocale: settings.defaultLocale,
      messages: {
        [settings.defaultLocale]: messages
      }
    })
    return this
  }

  /**
   * Configure bootstrap-vue plugin
   * @returns {Core} the current instance of Core
   */
  useBootstrapVue() {
    this.use(BootstrapVue, {
      BPopover: {
        boundaryPadding: 14
      }
    })
    return this
  }

  /**
   * Configure vue-router plugin
   * @returns {Core} the current instance of Core
   */
  useRouter() {
    this.use(VueRouter)
    this.router = new VueRouter(router)
    guards(this)
    return this
  }

  /**
   * Configure most common Vue plugins (Murmur, VueScrollTo)
   * @returns {Core} the current instance of Core
   */
  useCommons() {
    // Common plugins
    this.use(Murmur)
    this.use(VueScrollTo)
    this.use(Shortkey)
    this.LocalVue.directive('shortkey', vShortkey)
    return this
  }

  /**
   * Configure vue-wait plugin
   * @returns {Core} the current instance of Core
   */
  useWait() {
    this.use(VueWait)
    this.wait = new VueWait({ useVuex: true })
    return this
  }

  /**
   * Add a $core property to the instance's Vue
   * @returns {Core} the current instance of Core
   */
  useCore() {
    const core = this
    this.use(
      class VueCore {
        static install(Vue) {
          Vue.prototype.$core = core
        }
      }
    )
    return this
  }

  /**
   * Load settings from the server and instantiate most the application configuration.
   * @async
   * @fullfil {Core} - The instance of the core application
   * @reject {Object} - The Error object
   * @returns {Promise<Object>}
   */
  async configure() {
    try {
      // Murmur exposes a config attribute which share a Config object
      // with the current vue instance.
      // First, merge Murmur settings with the vue app settings:
      this.config.merge(settings)
      // Then, the backend can yet override some configuration.
      this.config.merge(await this.getSettings())
      // Finally, load the user into a specific attribute.
      this.config.set('user', await this.getUser())
      // Load the locale
      this.loadLocale(this.store.state.app.locale ?? 'en')
      // Old a promise that is resolved when the core is configured
      return this.ready && this._readyResolve(this)
    } catch (error) {
      return this.ready && this._readyReject(error)
    }
  }

  /**
   * Mount the instance's vue application
   * @param {String} [selector=#app] - Query selector to the mounting point
   * @returns {Vue} The instantiated Vue
   */
  mount(selector = '#app') {
    // Render function returns a router-view component by default
    const render = (h) => h(App)
    // We do not necessarily use the default Vue so we can use this function
    // from our unit tests
    const vm = new this.LocalVue({
      render,
      i18n: this.i18n,
      store: this.store,
      router: this.router,
      wait: this.wait
    }).$mount(selector)
    // Return an instance of the Vue constructor we receive.
    return vm
  }

  /**
   * Build a promise to be resolved when the application is configured.
   */
  defer() {
    this._ready = new Promise((resolve, reject) => {
      this._readyResolve = resolve
      this._readyReject = reject
    })
  }

  /**
   * Get the current signed user.
   * @async
   * @param {Boolean} cache - Cache the result from the API
   * @fullfil {Object} Current user
   * @type {Promise<Object>}
   */
  async getUser(cache = true) {
    if (!User.exists() || !cache) {
      await User.api().me()
    }
    return User.me()
  }

  /**
   * Get settings from the backend
   * @async
   * @param {Boolean} cache - Cache the result from the API
   * @fullfil {Object} Current user
   * @type {Promise<Object>}
   */
  async getSettings(cache = true) {
    if (!Setting.exists() || !cache) {
      await Setting.api().get()
    }
    return Setting.allAsObject()
  }

  /**
   * Append the given title to the page title
   * @param {String} title - Title to append to the page
   * @param {String} [suffix=Prophecies] - Suffix to the title
   */
  setPageTitle(title = null, suffix = 'Prophecies') {
    if (document && document.title) {
      document.title = title ? `${title} - ${suffix}` : suffix
    }
  }

  /**
   * Get a promise that is resolved when the application is ready
   * @fullfil {Object} The actual application core instance.
   * @type {Promise<Object>}
   */
  get ready() {
    if (!this._ready) {
      this.defer()
    }
    return this._ready
  }

  /**
   * The application core instance
   * @type {Core}
   */
  get core() {
    return this
  }

  /**
   * The Vue class to instantiate the application with
   * @type {Vue}
   */
  get localVue() {
    return this.LocalVue
  }

  /**
   * The Vuex instance
   * @type {Vuex.Store}
   */
  get store() {
    return store
  }

  /**
   * The configuration object provided by Murmur
   * @type {Object}
   */
  get config() {
    return Murmur.config
  }

  /**
   * instantiate a Core class (useful for chaining usage or mapping)
   * @param {...Mixed} options - Options to pass to the Core constructor
   * @returns {Core}
   */
  static init(...options) {
    return new Core(...options)
  }
}

export default Core
