import {
    createLocalVue,
    shallowMount
  } from '@vue/test-utils'
import Core from '@/core'
import StatsList from '@/views/StatsList'

describe('StatsList', () => {
    let wrapper

    beforeEach(async () => {
        const localVue = createLocalVue()
        // Configure the local vue with plugins
        const { wait, store } = Core.init(localVue).useAll()
        const stubs = ['app-waiter']
        
        const options = {
            stubs,
            localVue,
            store,
            wait
        }
    
        wrapper = await shallowMount(StatsList, options)
      })

    afterEach(async () => {
        await wrapper.destroy()
    })
    describe('Sort by task', () => {
        it('Shows sort dropdown', () => {
            const element = wrapper.find('stats-sort-dropdown-stub')
            expect(element.exists()).toBeTruthy()
        })
     
    })
})