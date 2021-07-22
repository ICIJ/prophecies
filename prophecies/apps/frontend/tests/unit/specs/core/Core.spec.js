import Murmur from '@icij/murmur'
import { createLocalVue } from '@vue/test-utils'
import Vue from 'vue'
import VueI18n from 'vue-i18n'
import VueRouter from 'vue-router'
import Vuex from 'vuex'

import api from '@/api'
import { Core } from '@/core'

jest.mock('@/api', () => {
  return {
    get: jest.fn().mockResolvedValue({ data: {} })
  }
})

describe('Core', () => {
  let localVue

  beforeEach(() => {
    localVue = createLocalVue()
  })

  beforeEach(() => {
    const app = document.createElement('div')
    app.setAttribute('id', 'core')
    document.body.appendChild(app)
    api.get.mockClear()
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
    const { router } = Core.init(localVue).useAll()
    expect(router).toBeInstanceOf(VueRouter)
  })

  it('should expose the VueI18n', () => {
    const { i18n } = Core.init(localVue).useAll()
    expect(i18n).toBeInstanceOf(VueI18n)
  })

  it('should expose the store', () => {
    const { store } = Core.init(localVue).useAll()
    expect(store).toBeInstanceOf(Vuex.Store)
  })

  it('should not expose the router if it is not installed', () => {
    const { router } = Core.init(localVue)
    expect(router).not.toBeInstanceOf(VueRouter)
  })

  it('should not expose the VueI18n if it is not installed', () => {
    const { i18n } = Core.init(localVue)
    expect(i18n).not.toBeInstanceOf(VueI18n)
  })

  it('should expose the config from Murmur', () => {
    const { config } = Core.init(localVue).useAll()
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
})
