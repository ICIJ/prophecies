import { createLocalVue, mount } from '@vue/test-utils'
import AppSidebar from '@/components/AppSidebar'
import Core from '@/core'

describe('AppSidebar', () => {
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
    wrapper = mount(AppSidebar, { i18n, localVue, router })
  })

  it('should display the backend value of `appName` as app name', () => {
    const brandName = wrapper.find('.app-sidebar__brand__app-name')
    expect(brandName.text()).toBe('Data Fact Check')
  })

  it('should display the config value of `appName` as app name', async () => {
    config.set('appName', 'Prophecies')
    await wrapper.vm.$nextTick()
    const brandName = wrapper.find('.app-sidebar__brand__app-name')
    expect(brandName.text()).toBe('Prophecies')
  })

  it('should display the backend value of `orgName` as org name', () => {
    const brandName = wrapper.find('.app-sidebar__brand__org-name')
    expect(brandName.text()).toBe('ICIJ.org')
  })

  it('should display the config value of `orgName` as org name', async () => {
    config.set('orgName', 'ICIJ')
    await wrapper.vm.$nextTick()
    const brandName = wrapper.find('.app-sidebar__brand__org-name')
    expect(brandName.text()).toBe('ICIJ')
  })
})
