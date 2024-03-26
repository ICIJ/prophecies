import { createLocalVue, shallowMount } from '@vue/test-utils'

import Core from '@/core'
import StatsList from '@/views/StatsList'

describe('StatsList', () => {
  describe('Show the stat list page', () => {
    let wrapper
    let options

    beforeEach(async () => {
      const localVue = createLocalVue()

      // Configure the local vue
      const core = await Core.init(localVue).useAll()
      const { i18n, wait, store, router } = core
      const propsData = { teamTaskStats: true }
      const stubs = ['router-link', 'router-view', 'app-waiter']
      // Finally, instanciate the component
      options = {
        i18n,
        localVue,
        propsData,
        router,
        stubs,
        store,
        wait
      }
      await core.configure()

      wrapper = shallowMount(StatsList, options)
      await wrapper.vm.setup()
    })

    it('should show 4 extended cards', async () => {
      const taskCards = wrapper.findAll('.stats-list__task-card')
      expect(taskCards).toHaveLength(4)
    })
    // TODO: add test on sort
  })
})
