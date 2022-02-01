import { createLocalVue, shallowMount } from '@vue/test-utils'
import StatsByRound from '@/components/StatsByRound'
import Core from '@/core'

describe('StatsByRound', () => {
  describe('Show stats by round', () => {
    let wrapper

    function createContainer () {
      const div = document.createElement('div')
      document.body.appendChild(div)
      return div
    }
    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const propsData = {
        extended: true,
        round: 1,
        progress: 80,
        summary: [
          { name: 'Incorrect', value: 'incorrect', progress: 25 },
          { name: 'Correct', value: 'correct', progress: 75 },
          { name: 'Unknown', value: 'unknown', progress: 0 }
        ],
        progressByUser: [{ checker: { username: 'django' }, done: 5, pending: 0, progress: 100 }, { checker: { username: 'olivia' }, done: 2, pending: 2, progress: 50 }]
      }

      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const { i18n } = core
      // Finally, instanciate the component
      wrapper = shallowMount(StatsByRound, { attachTo, localVue, propsData, i18n })
    })

    it('should display round 1', () => {
      const elements = wrapper.find('.stats-by-round__progress')
      expect(elements.text()).toBe('Round 1')
    })
    it('should display round progress bar (extended)', () => {
      const element = wrapper.find('b-progress-stub')
      expect(element.attributes('value')).toBe('80')
    })
    it('should display stats by user component', () => {
      const element = wrapper.findAll('stats-by-users-stub')
      expect(element.exists()).toBeTruthy()
    })

    it('should display the choice badges and their correctness', () => {
      const elements = wrapper.findAll('.stats-by-round__summary__choice')
      expect(elements).toHaveLength(3)
      const choiceBadges = wrapper.findAll('.stats-by-round__summary__choice choice-badge-stub')
      expect(choiceBadges).toHaveLength(3)

      expect(elements.wrappers[0].text()).toEqual('25%')
      expect(elements.wrappers[1].text()).toEqual('75%')
      expect(elements.wrappers[2].text()).toEqual('0%')
    })
  })
})
