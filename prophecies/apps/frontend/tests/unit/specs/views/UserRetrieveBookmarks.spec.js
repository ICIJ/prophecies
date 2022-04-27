import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import User from '@/models/User'
import UserRetrieveBookmarks from '@/views/UserRetrieveBookmarks'

describe('Bookmarks', () => {
  let wrapper

  beforeAll(async () => {
    await User.api().get()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    const { i18n, wait, store, router } = Core.init(localVue).useAll()

    const query = {
      'filter[project]': null,
      'filter[task]': null
    }
    const propsData = { query, username: 'django' }

    wrapper = shallowMount(UserRetrieveBookmarks, {
      i18n,
      localVue,
      propsData,
      store,
      router,
      wait
    })

    await wrapper.vm.setup()
  })

  it('should display bookmarked items', async () => {
    const bookmarks = await wrapper.findAll('task-record-review-card-stub')
    expect(wrapper.vm.taskRecordReviewIds).toHaveLength(5)
    expect(bookmarks).toHaveLength(5)
  })

  it('should display bookmarked items grouped by projects then by tasks', async () => {
    const project = await wrapper.findAll('.user-retrieve-bookmarks__project')
    expect(project).toHaveLength(2)
    expect(project.at(0).find('h1').text()).toContain('Chronos')
    expect(project.at(1).find('h1').text()).toContain('Demeter')

    expect(wrapper.vm.taskIds).toHaveLength(2)
    expect(project.at(0).find('h2').text()).toContain('Addresses')
    expect(project.at(1).find('h2').text()).toContain('Shops')
  })

  it('should apply filters', async () => {
    await wrapper.setProps({ query: { 'filter[project]': '2' } })

    let project = await wrapper.findAll('.user-retrieve-bookmarks__project')
    expect(project).toHaveLength(1)
    expect(project.at(0).find('h1').text()).toContain('Demeter')
    expect(project.at(0).find('h2').text()).toContain('Shops')
    expect(project.at(0).findAll('task-record-review-card-stub')).toHaveLength(3)

    await wrapper.setProps({ query: { 'filter[task]': '1' } })
    project = await wrapper.findAll('.user-retrieve-bookmarks__project')
    expect(project).toHaveLength(1)
    expect(project.at(0).find('h1').text()).toContain('Chronos')
    expect(project.at(0).find('h2').text()).toContain('Addresses')
    expect(project.at(0).findAll('task-record-review-card-stub')).toHaveLength(2)
  })

  it('should show the message "No bookmarks" when list is empty', async () => {
    await wrapper.setData({ taskRecordReviewIds: [] })
    expect(wrapper.vm.taskRecordReviewIds).toHaveLength(0)
    const element = wrapper.find('.user-retrieve-bookmarks__empty')
    expect(element.exists()).toBeTruthy()
    expect(element.attributes().title).toBe('No records bookmarked yet')
  })
})
