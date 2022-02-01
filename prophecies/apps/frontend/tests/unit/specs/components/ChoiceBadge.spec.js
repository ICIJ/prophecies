import { createLocalVue, shallowMount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import ChoiceBadge from '@/components/ChoiceBadge'

describe('ChoiceBadge', () => {
  let wrapper

  function createContainer () {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  beforeEach(() => {
    const attachTo = createContainer()
    const localVue = createLocalVue()
    const propsData = { name: 'Unknown', value: 'unknown' }
    // Configure the local vue with plugins
    Core.init(localVue).useAll()
    wrapper = shallowMount(ChoiceBadge, { attachTo, localVue, propsData })
  })

  it('should only show the first letter of the status', () => {
    const firstCheckerBadge = wrapper.find('.choice__badge :not(.sr-only)')
    expect(firstCheckerBadge.text()).toBe('Unknown')
    const firstCheckerBadgeEnd = wrapper.find('.choice__badge .sr-only')
    expect(firstCheckerBadgeEnd.text()).toBe('nknown')
  })

  it('should show the choice in the tooltip', () => {
    const firstCheckerBadge = wrapper.find('.choice__tooltip')
    expect(firstCheckerBadge.text()).toBe('Unknown')
  })
})
