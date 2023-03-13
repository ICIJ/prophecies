import {createLocalVue, shallowMount} from '@vue/test-utils'
import Murmur from '@icij/murmur'
import Vue from 'vue'
import VueI18n from 'vue-i18n'
import VueRouter from 'vue-router'
import Vuex from 'vuex'

import {rest, server} from '../../mocks/server'
import Core from '@/core'
import Setting from '@/models/Setting'

jest.mock('@/router', () => ({router: {routes: []}}))
jest.mock('@/utils/icons', () => {
  const BarIcon = {name: 'BarIcon', template: '<i></i>'}
  const FooIcon = {name: 'FooIcon', template: '<i></i>'}
  return {
    ...jest.requireActual('@/utils/icons'),
    BarIcon,
    FooIcon
  }
})

describe('Core', () => {
  let localVue

  beforeEach(() => {
    const app = document.createElement('div')
    app.setAttribute('id', 'core')
    document.body.appendChild(app)
    localVue = createLocalVue()
    // Clear Murmur config
    Murmur.config.set('foo', null)
    // Mock settings
    server.use(rest.get('/api/v1/settings', (req, res, ctx) => {
      return res.once(ctx.json({
        data: [
          {type: 'Setting', id: '1', attributes: {key: 'foo', value: 'bar'}}
        ]
      }))
    }))
  })

  afterEach(() => {
    server.resetHandlers()
    Setting.deleteAll()
  })

  it('should instantiate the Core class', () => {
    const core = new Core(localVue)
    expect(core).toBeInstanceOf(Core)
  })

  it('should instantiate the Core class using a static method', () => {
    const core = Core.init(localVue)
    expect(core).toBeInstanceOf(Core)
  })

  it('should expose the router', () => {
    const {router} = Core.init(localVue).useAll()
    expect(router).toBeInstanceOf(VueRouter)
  })

  it('should expose the VueI18n', () => {
    const {i18n} = Core.init(localVue).useAll()
    expect(i18n).toBeInstanceOf(VueI18n)
  })

  it('should expose the store', () => {
    const {store} = Core.init(localVue).useAll()
    expect(store).toBeInstanceOf(Vuex.Store)
  })

  it('should not expose the router if it is not installed', () => {
    const {router} = Core.init(localVue)
    expect(router).not.toBeInstanceOf(VueRouter)
  })

  it('should not expose the VueI18n if it is not installed', () => {
    const {i18n} = Core.init(localVue)
    expect(i18n).not.toBeInstanceOf(VueI18n)
  })

  it('should expose the config from Murmur', () => {
    const {config} = Core.init(localVue).useAll()
    expect(config).toBe(Murmur.config)
  })

  it('should mount the app on a specific element', () => {
    const core = Core.init(localVue).useAll()
    const vm = core.mount('#core')
    expect(vm).toBeInstanceOf(Vue)
  })

  it('should resolve the `ready` promise after the core was configured', async () => {
    // Create and configure the core
    const core = Core.init(localVue).useAll()
    // For `ready` to be resolved, the core must configure
    await core.configure()
    await expect(core.ready).resolves.toBe(core)
  })

  it('should install the internal `VueCore` plugin', () => {
    // Create and configure the core
    const core = Core.init(localVue).useAll()
    const vm = core.mount('#core')
    expect(vm.$core).toBeInstanceOf(Core)
  })

  it('should copy settings from the backend into Murmur config', async () => {
    // Create and configure the core
    const core = Core.init(localVue).useAll()
    expect(core.config.get('foo', null)).toBe(null)
    await core.configure()
    expect(core.config.get('foo', null)).toBe('bar')
  })

  it('should transform settings list into an object', async () => {
    jest.restoreAllMocks()
    // Mock settings
    server.use(rest.get('/api/v1/settings', (req, res, ctx) => {
      return res.once(ctx.json({
        data: [
          {type: 'Setting', id: '1', attributes: {key: 'searchEngine', value: 'https://duckduckgo.com'}}
        ]
      }))
    }))
    const core = new Core(localVue)
    const settings = await core.getSettings()
    expect(settings).toBeInstanceOf(Object)
    expect(settings.searchEngine).toBe('https://duckduckgo.com')
  })

  it('should register all icons exported by the @/utils/icons', () => {
    Core.init(localVue)
    const Component = {render: h => h('bar-icon')}
    const vm = shallowMount(Component, {localVue})
    expect(vm.findComponent({name: 'bar-icon'}).exists()).toBeTruthy()
    expect(vm.findComponent({name: 'foo-icon'}).exists()).toBeFalsy()
  })
})
