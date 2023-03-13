import {createLocalVue, mount} from '@vue/test-utils'
import Core from '@/core'
import TaskStatsCardDetailed from '@/components/TaskStatsCardDetailed'
import Task from '@/models/Task'
import User from '@/models/User'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'
import TaskUserStatistics from '@/models/TaskUserStatistics'

describe('TaskStatsCardDetailed', () => {
  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  describe('Show the task card with round details', () => {
    let wrapper
    beforeAll(async () => {
      await Task.api().get()
      await TaskUserChoiceStatistics.api().get()
      await TaskUserStatistics.api().get()
      await User.api().get()
    })
    beforeEach(async () => {
      const attachTo = createContainer()

      const localVue = createLocalVue()

      // Configure the local vue
      const core = await Core.init(localVue).useAll()
      const {i18n, wait, store} = core
      const propsData = {taskId: '1', team: false}
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
    it('should display stats by user component for first 2 rounds', () => {
      const element = wrapper.findAll('.stats-by-round')
      expect(element).toHaveLength(3)
      const firstStatsByUsers = element.at(0).find('.stats-by-users')
      expect(firstStatsByUsers.exists()).toBeTruthy()
      const secondStatsByUsers = element.at(1).find('.stats-by-users')
      expect(secondStatsByUsers.exists()).toBeTruthy()
      const thirdStatsByUsers = element.at(2).find('.stats-by-users')
      expect(thirdStatsByUsers.exists()).toBeFalsy()
    })

    it('should display "No record assigned" message for round 3', () => {
      const element = wrapper.findAll('.stats-by-round')
      expect(element).toHaveLength(3)
      const thirdStatsByUsers = element.at(2).find('.stats-by-round__progress__value--no-record')
      expect(thirdStatsByUsers.exists()).toBeTruthy()
    })

    it('should display stats by user component for 2 rounds ', () => {
      const element = wrapper.findAll('.stats-by-users')
      expect(element.exists()).toBeTruthy()
      expect(element).toHaveLength(2)
    })

    describe('first round of task 1', () => {
      let card, rounds, round
      beforeEach(async () => {
        await wrapper.setProps({team: true})
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
      /*
        Task 3 round 1
        user | Correct | Incorrect | Unknown | Total
        u1      c:39        i:1         u:3     t:43
        u2      c:3         i:1         u:1     t:5
        total   c:42        i:2         u:4     t:48
        */
      let card, rounds, round
      beforeEach(async () => {
        await wrapper.setProps({taskId: '3'})
        card = wrapper.find('.stats-list__task-card')
        rounds = card.findAll('.stats-list__task-card__round')
        round = rounds.at(0)
      })
      describe('show details of team', () => {
        beforeEach(async () => {
          await wrapper.setProps({team: true})
        })
        it('should show the stats of 2 checkers', async () => {
          const checkersRows = round.findAll('.stats-by-users__row')

          expect(checkersRows).toHaveLength(2)
          expect(checkersRows.at(0).text()).toContain('43%')
          expect(checkersRows.at(1).text()).toContain('5%')
        })

        it('should display the total team progress of 6% on this round', () => {
          const totalRow = round.find('.stats-by-users__total')
          const totalProgress = totalRow.find('.stats-by-users__row__progress')
          expect(totalProgress.text()).toBe('24%')
        })

        it('should display the team choice percentage for the first choice Correct 88%', () => {
          const teamChoice0 = round.findAll('.stats-by-round__summary__choice').at(0)
          expect(teamChoice0.text()).toBe('Correct 88%')
        })
        it('should display the team choice percentage for the first choice Incorrect 4%', () => {
          const teamChoice1 = round.findAll('.stats-by-round__summary__choice').at(1)
          expect(teamChoice1.text()).toBe('Incorrect 4%')
        })
        it('should display the team choice percentage for the first choice Unknown 8%', () => {
          const teamChoice2 = round.findAll('.stats-by-round__summary__choice').at(2)
          expect(teamChoice2.text()).toBe("Don't know 8%")
        })

        it('should display the total team progress of 24% on this round', () => {
          const totalRow = round.find('.stats-by-users__total')
          const totalProgress = totalRow.find('.stats-by-users__row__progress')
          expect(totalProgress.text()).toBe('24%')
        })

        it('should row total only on team tab ', async () => {
          let totalRow = round.find('.stats-by-users__total')
          expect(totalRow.exists()).toBeTruthy()
          await wrapper.setProps({team: false})
          totalRow = round.find('.stats-by-users__total')
          expect(totalRow.exists()).toBeFalsy()
        })
      })

      describe('user stats', () => {
        it('should show the stats of checker with id 1 ', async () => {
          await wrapper.setProps({checkerId: '1'})
          const checkersRows = round.findAll('.stats-by-users__row')

          expect(checkersRows).toHaveLength(1)
          expect(checkersRows.at(0).text()).toContain('43%')
        })

        it('should display the checker 2 progress on this round', async () => {
          await wrapper.setProps({checkerId: '2'})

          const totalProgress = round.find('.stats-by-users__row__progress')
          expect(totalProgress.text()).toBe('5%')
        })
        it('should display the user 2 choice percentage for the first choice Correct 60%', async () => {
          await wrapper.setProps({checkerId: '1'})
          const user1 = round.findAll('.stats-by-round__summary__choice').at(0)
          expect(user1.text()).toBe('Correct 91%')
          await wrapper.setProps({checkerId: '2'})
          const user2 = round.findAll('.stats-by-round__summary__choice').at(0)
          expect(user2.text()).toBe('Correct 60%')
        })
        it('should display the user 1 choice percentage for the first choice Correct 91%', async () => {
          await wrapper.setProps({checkerId: '1'})
          const user1 = round.findAll('.stats-by-round__summary__choice').at(0)
          expect(user1.text()).toBe('Correct 91%')
        })
        it('should display the total user progress of 5% on this round', async () => {
          await wrapper.setProps({checkerId: '2'})
          const checkersRows = round.findAll('.stats-by-users__row')
          expect(checkersRows).toHaveLength(1)
          expect(checkersRows.at(0).text()).toContain('django')

          const totalProgress = round.find('.stats-by-users__row__progress')
          expect(totalProgress.text()).toBe('5%')
        })
      })
    })
  })
})
