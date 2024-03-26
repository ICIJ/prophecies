import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import HistoryList from '@/components/HistoryList'

describe('HistoryList', () => {
  let wrapper

  const localVue = createLocalVue()
  // Configure the local vue with plugins
  const { i18n, store, wait } = Core.init(localVue).useAll()

  it('should display a title if available slot', async () => {
    wrapper = await shallowMount(HistoryList, {
      i18n,
      wait,
      localVue,
      store,
      slots: {
        title: 'Test Title'
      }
    })

    const elem = wrapper.find('.history-list__title')
    expect(elem.exists()).toBeTruthy()
    expect(elem.text()).toContain('Test Title')
  })

  it("shouldn't display a title if unavailable slot", async () => {
    wrapper = await shallowMount(HistoryList, {
      i18n,
      wait,
      localVue,
      store
    })

    const elem = wrapper.find('.history-list__title')
    expect(elem.exists()).toBeFalsy()
  })
})
