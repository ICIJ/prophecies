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
    // Mock Core methods that use the backend
    jest.spyOn(Core.prototype, 'getUser').mockResolvedValue({ })
    jest.spyOn(Core.prototype, 'getSettings').mockResolvedValue({ appName: 'Data Fact Check', orgName: 'ICIJ.org' })
    // Configure the local vue
    const core = Core.init(localVue).useAll()
    // Load the settings
    await core.configure()
    // Those core properties must be available for each test
    i18n = core.i18n
    config = core.config
    router = core.router
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  it('should display the backend value of `appName` as app name', () => {
    wrapper = mount(AppSidebar, { i18n, localVue, router })
    const brandName = wrapper.find('.app-sidebar__brand__app-name')
    expect(brandName.text()).toBe('Data Fact Check')
  })

  it('should display the config value of `appName` as app name', () => {
    config.set('appName', 'Prophecies')
    wrapper = mount(AppSidebar, { i18n, localVue, router })
    const brandName = wrapper.find('.app-sidebar__brand__app-name')
    expect(brandName.text()).toBe('Prophecies')
  })

  it('should display the backend value of `orgName` as org name', () => {
    wrapper = mount(AppSidebar, { i18n, localVue, router })
    const brandName = wrapper.find('.app-sidebar__brand__org-name')
    expect(brandName.text()).toBe('ICIJ.org')
  })

  it('should display the config value of `orgName` as org name', () => {
    config.set('orgName', 'ICIJ')
    wrapper = mount(AppSidebar, { i18n, localVue, router })
    const brandName = wrapper.find('.app-sidebar__brand__org-name')
    expect(brandName.text()).toBe('ICIJ')
  })
})
