import { createLocalVue, mount } from '@vue/test-utils'

import AppBrand from '@/components/AppBrand'
import Core from '@/core'

describe('AppBrand', () => {
  let localVue
  let wrapper
  let i18n
  let config
  let router

  beforeEach(async () => {
    localVue = createLocalVue()
    // Configure the local vue
    const core = Core.init(localVue).useAll()
    // Load the settings
    await core.configure()
    // Those core properties must be available for each test
    i18n = core.i18n
    config = core.config
    router = core.router
    wrapper = mount(AppBrand, { i18n, localVue, router })
  })

  it('should display the backend value of `appName` as app name', () => {
    const brandName = wrapper.find('.app-brand__app-name__logo')
    expect(brandName.attributes('alt')).toBe('Data Fact Check')
  })

  it('should display the config value of `appName` as app name', async () => {
    config.set('appName', 'Prophecies')
    await wrapper.vm.$nextTick()
    const brandName = wrapper.find('.app-brand__app-name__logo')
    expect(brandName.attributes('alt')).toBe('Prophecies')
  })

  it('should display the backend value of `orgName` as org name', () => {
    const brandName = wrapper.find('.app-brand__org-name')
    expect(brandName.text()).toBe('ICIJ.org')
  })

  it('should display the config value of `orgName` as org name', async () => {
    config.set('orgName', 'ICIJ')
    await wrapper.vm.$nextTick()
    const brandName = wrapper.find('.app-brand__org-name')
    expect(brandName.text()).toBe('ICIJ')
  })
})
