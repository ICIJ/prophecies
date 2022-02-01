import {
  createLocalVue,
  mount
} from '@vue/test-utils'
import Core from '@/core'
import StatsList from '@/views/StatsList'
import Task from '@/models/Task'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'

describe('StatsList', () => {
  function createContainer () {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  describe('Show the stat list page', () => {
    let wrapper
    let options

    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()

      // Configure the local vue
      const core = await Core.init(localVue).useAll()
      const { i18n, wait, store, router } = core
      const propsData = { teamTaskStats: true }
      const stubs = ['router-link', 'router-view', 'app-waiter']
      // Finally, instanciate the component
      options = {
        i18n,
        attachTo,
        localVue,
        propsData,
        router,
        stubs,
        store,
        wait
      }
      await core.configure()

      wrapper = mount(StatsList, options)
      await wrapper.vm.setup()
    })

    afterEach(async () => {
      await wrapper.destroy()

      Task.deleteAll()
      TaskUserStatistics.deleteAll()
      TaskUserChoiceStatistics.deleteAll()
    })
    it('should show 4 extended cards', async () => {
      const taskCards = wrapper.findAll('.stats-list__task-card')
      expect(taskCards).toHaveLength(4)
    })
    it('should show the first card with 3 rounds', async () => {
      const firstCard = wrapper.findAll('.stats-list__task-card').at(0)
      const rounds = firstCard.findAll('.stats-list__task-card__round')
      expect(rounds).toHaveLength(3)
    })

    describe('first round of first card', () => {
      let card, rounds, round
      beforeEach(() => {
        card = wrapper.findAll('.stats-list__task-card').at(0)
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

    describe('first round of third card', () => {
      let card, rounds, round
      beforeEach(() => {
        card = wrapper.findAll('.stats-list__task-card').at(2)
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
        await wrapper.setData({ teamTaskStats: false })
        const userChoice1 = round.findAll('.stats-by-round__summary__choice').at(0)
        expect(userChoice1.text()).toBe('Correct 60%')
      })

      it('should display the total team progress of 24% on this round', () => {
        const totalRow = round.find('.stats-by-users__total')
        const totalProgress = totalRow.find('.stats-by-users__row__progress')
        expect(totalProgress.text()).toBe('24%')
      })
      it('should display the total user progress of 33% on this round', async () => {
        await wrapper.setData({ teamTaskStats: false })
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
