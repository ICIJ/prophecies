import {
    createLocalVue,
    mount,
    shallowMount
  } from '@vue/test-utils'
import Core from '@/core'
import StatsSortDropdown from '@/components/StatsSortDropdown'

describe('StatsSortDropdown', () => {
    let wrapper
  describe('mount',()=>{

    beforeEach(async () => {
      const localVue = createLocalVue()

      // Configure the local vue with plugins
      const { wait, store, router } = Core.init(localVue).useAll()
      
      
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
    
  describe('shallowmount',()=>{
    function createContainer() {
      const div = document.createElement('div')
      document.body.appendChild(div)
      return div
    }
    beforeEach(async () => {

      const attachTo = createContainer()
      const localVue = createLocalVue()

      // Configure the local vue with plugins
      const { wait, store, router } = Core.init(localVue).useAll()
      
      
      const $route = {
          path: '/some/path'
      }
      const options = {
        attachTo,
          localVue,
          router,
          mocks: {
              $route
          },
      }
        
      wrapper = await shallowMount(StatsSortDropdown, options)
    })

    it('updates URL when sort option is changed', () => {
      console.log()
      const url = wrapper.vm.$route.path
      console.log(url)
      expect(true).toBeFalsy()    
    })
  })
  



})