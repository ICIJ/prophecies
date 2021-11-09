import {
    createLocalVue,
    mount
  } from '@vue/test-utils'
import Core from '@/core'
import StatsSortDropdown from '@/components/StatsSortDropdown'

describe('StatsSortDropdown', () => {
    let wrapper

    beforeEach(async () => {
        const localVue = createLocalVue()
        // Configure the local vue with plugins
        const { wait, store } = Core.init(localVue).useAll()
        
        const options = {
            localVue,
        }
    
        wrapper = await mount(StatsSortDropdown, options)
      })


    it('selects the ID as the default sorting value', ()=>{
        const selectedElement = wrapper.find('.multiselect__single')
        expect(selectedElement.text()).toBe('ID (default)')
    })

})