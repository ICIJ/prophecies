import {
  createLocalVue,
  mount
} from '@vue/test-utils'
import Core from '@/core'
import TaskStatsCardDetailed from '@/components/TaskStatsCardDetailed'
import Task from '@/models/Task'
import User from '@/models/User'

describe('TaskStatsCardDetailed', () => {
  function createContainer () {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }
  describe('Show the task card with round details', () => {
    let wrapper
    beforeAll(async () => {
      await Task.api().get()
      await User.api().me()
    })
    beforeEach(async () => {
      const attachTo = createContainer()

      const localVue = createLocalVue()

      // Configure the local vue
      const core = await Core.init(localVue).useAll()
      const { i18n, wait, store } = core
      const propsData = { team: true, taskId: '1' }
      const stubs = ['router-link', 'app-waiter']
      // Finally, instanciate the component
      const options = {
        i18n,
        localVue,
        attachTo,
        propsData,
        stubs,
        store,
        wait
      }
      await core.configure()

      wrapper = mount(TaskStatsCardDetailed, options)
      await wrapper.vm.setup()
    })

    it('should show the task 1 card with 3 rounds', async () => {
      const firstCard = wrapper.find('.stats-list__task-card')
      const rounds = firstCard.findAll('.stats-list__task-card__round')
      expect(rounds).toHaveLength(3)
    })

    describe('first round of task 1', () => {
      let card, rounds, round
      beforeEach(() => {
        card = wrapper.find('.stats-list__task-card')
        rounds = card.findAll('.stats-list__task-card__round')
        round = rounds.at(0)
      })

      it('should show the stats of 1 checker', async () => {
        const checkersRows = round.findAll('.stats-by-users__row')
        expect(checkersRows).toHaveLength(1)
      })
      it('should display the total team progress of 6% on this round', () => {
        const totalRow = round.find('.stats-by-users__total')
        const totalProgress = totalRow.find('.stats-by-users__row__progress')
        expect(totalProgress.text()).toBe('6%')
      })
    })

    describe('first round of task 3', () => {
      let card, rounds, round
      beforeEach(async () => {
        await wrapper.setProps({ taskId: '3' })
        card = wrapper.find('.stats-list__task-card')
        rounds = card.findAll('.stats-list__task-card__round')
        round = rounds.at(0)
      })

      it('should show the stats of 2 checkers', async () => {
        const checkersRows = round.findAll('.stats-by-users__row')
        expect(checkersRows).toHaveLength(2)
      })

      it('should display the team choice percentage for the first choice Correct 50%', () => {
        const teamChoice1 = round.findAll('.stats-by-round__summary__choice').at(0)
        expect(teamChoice1.text()).toBe('Correct 88%')
      })

      it('should display the user choice percentage for the first choice Correct 60%', async () => {
        await wrapper.setProps({ team: false })
        const userChoice1 = round.findAll('.stats-by-round__summary__choice').at(0)
        expect(userChoice1.text()).toBe('Correct 60%')
      })

      it('should display the total team progress of 24% on this round', () => {
        const totalRow = round.find('.stats-by-users__total')
        const totalProgress = totalRow.find('.stats-by-users__row__progress')
        expect(totalProgress.text()).toBe('24%')
      })
      it('should display the total user progress of 33% on this round', async () => {
        await wrapper.setProps({ team: false })
        const checkersRows = round.findAll('.stats-by-users__row')
        expect(checkersRows).toHaveLength(1)
        expect(checkersRows.at(0).text()).toContain('django')

        const totalRow = round.find('.stats-by-users__total')
        const totalProgress = totalRow.find('.stats-by-users__row__progress')
        expect(totalProgress.text()).toBe('5%')
      })
    })
  })
})
