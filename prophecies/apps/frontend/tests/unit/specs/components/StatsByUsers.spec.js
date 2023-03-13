import {createLocalVue, shallowMount} from '@vue/test-utils'
import StatsByUsers from '@/components/StatsByUsers'
import Core from '@/core'

describe('StatsByUsers', () => {
  describe('Show list of users and the total', () => {
    let wrapper
    beforeEach(async () => {
      const localVue = createLocalVue()
      const propsData = {
        users: [{name: 'django', done: 5, pending: 0, progress: 100}, {
          name: 'olivia',
          done: 2,
          pending: 2,
          progress: 50
        }]
      }
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const {i18n} = core
      // Finally, instanciate the component
      wrapper = shallowMount(StatsByUsers, {localVue, propsData, i18n})
    })

    it('should show two users stats', () => {
      const elements = wrapper.findAll('.stats-by-users__row')
      expect(elements).toHaveLength(2)
    })
    it('should display user name', () => {
      const element = wrapper.find('.stats-by-users__row__username')
      expect(element.text()).toEqual('django')
    })

    it('should display number of done reviews with the check icon', () => {
      const element = wrapper.find('.stats-by-users__row__done')
      expect(element.text()).toEqual('5')
      const checkIcon = element.find('check-icon-stub')
      expect(checkIcon.exists()).toBeTruthy()
    })
    it('computes the stats of given users', () => {
      const users = [{name: 'django', done: 5, pending: 0, progress: 100}, {
        name: 'olivia',
        done: 2,
        pending: 2,
        progress: 50
      }]
      const total = wrapper.vm.computeStats(users)
      expect(total.done).toEqual(7)
      expect(total.pending).toEqual(2)
      expect(total.progress).toEqual(75)
    })
  })
})
