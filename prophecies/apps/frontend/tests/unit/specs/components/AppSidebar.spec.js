import { createLocalVue, shallowMount } from '@vue/test-utils'
import AppBrand from '@/components/AppBrand'
import AppSidebar from '@/components/AppSidebar'
import AppVersion from '@/components/AppVersion'
import Core from '@/core'

describe('AppSidebar', () => {
  let localVue
  let wrapper

  beforeEach(async () => {
    localVue = createLocalVue()
    // Configure the local vue
    const core = Core.init(localVue).useAll()
    // Load the settings
    await core.configure()
    // Those core properties must be available for each test
    const { router, i18n } = core
    wrapper = shallowMount(AppSidebar, { i18n, router, localVue })
  })

  it('should display an AppBrand component', () => {
    const appBrand = wrapper.findComponent(AppBrand)
    expect(appBrand.exists()).toBeTruthy()
  })

  it('should display an AppVersion component', () => {
    const appVersion = wrapper.findComponent(AppVersion)
    expect(appVersion.exists()).toBeTruthy()
  })
})
