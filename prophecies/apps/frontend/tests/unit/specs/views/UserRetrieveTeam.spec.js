import { createLocalVue, mount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import User from '@/models/User'

import UserRetrieveTeam from '@/views/UserRetrieveTeam'
import UserCard from '@/components/UserCard'
import TaskStatsCardAllRounds from '@/components/TaskStatsCardAllRounds'

describe('UserRetrieveTeam', () => {
  let wrapper

  beforeAll(async () => {
    await User.api().get()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    const core = Core.init(localVue).useAll()
    const { i18n, wait, store } = core
    const stubs = ['router-link', 'app-waiter']
    const propsData = { username: 'olivia' }
    const options = {
      i18n,
      localVue,
      propsData,
      store,
      stubs,
      wait
    }
    await core.configure()

    wrapper = mount(UserRetrieveTeam, options)
    await wrapper.vm.setup()
  })

  afterEach(async () => {
    // Prevent a Vue warning in the next tick when the parentNode doesnt exist:
    // > TypeError: Cannot read property 'createElement' of null
    // @see https://stackoverflow.com/a/62262333
    wrapper.destroy()
  })

  it('should display card of teammate django (id:2) ', () => {
    const usercards = wrapper.findAllComponents(UserCard)
    expect(usercards).toHaveLength(1)
    expect(usercards.at(0).vm.userId).toBe('2')
  })

  it('should display a teammate with a stat component ', () => {
    const usercard = wrapper.findComponent(UserCard)
    const stats = usercard.findComponent(TaskStatsCardAllRounds)
    expect(stats.exists()).toBeTruthy()
  })
})
