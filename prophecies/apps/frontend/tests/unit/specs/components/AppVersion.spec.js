import { createLocalVue, mount } from '@vue/test-utils'
import AppVersion from '@/components/AppVersion'
import Core from '@/core'

describe('AppVersion', () => {
  let localVue
  let wrapper
  let i18n
  let config

  beforeEach(async () => {
    localVue = createLocalVue()
    // Configure the local vue
    const core = Core.init(localVue).useAll()
    // Load the settings
    await core.configure()
    // Those core properties must be available for each test
    i18n = core.i18n
    config = core.config
  })

  it('should display the backend version using the `version` config value', () => {
    wrapper = mount(AppVersion, { i18n, localVue })
    expect(wrapper.text()).toBe('Version 0.4.6')
  })

  it('should display the version "CANARY" using the `version` config value', () => {
    config.set('version', 'CANARY')
    wrapper = mount(AppVersion, { i18n, localVue })
    expect(wrapper.text()).toBe('Version CANARY')
  })

  it('should display the version "0.0.1" using the `version` config value', () => {
    config.set('version', '0.0.1')
    wrapper = mount(AppVersion, { i18n, localVue })
    expect(wrapper.text()).toBe('Version 0.0.1')
  })
})
