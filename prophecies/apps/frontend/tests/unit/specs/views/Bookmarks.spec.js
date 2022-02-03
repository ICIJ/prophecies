import {createLocalVue, shallowMount} from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import TaskRecordReview from '@/models/TaskRecordReview'
import Task from '@/models/Task'
import Bookmarks from '@/views/Bookmarks'
import User from '@/models/User'


describe('Bookmarks', () => {
  let wrapper

  beforeAll(async () => {
    await User.api().me()
    await TaskRecordReview.api().get()
    await Task.api().get()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    const { i18n, wait, store, router } = Core.init(localVue).useAll()

    const query = {
      'filter[project]': null,
      'filter[task]': null
    }
    const propsData = { query }

    wrapper = await shallowMount(Bookmarks, {
      i18n,
      localVue,
      propsData,
      store,
      router,
      wait
    })
  })

  afterEach(async () => {
    await TaskRecordReview.deleteAll()
    await Task.deleteAll()
    await wrapper.destroy()
  })

  it('should display bookmarked items', async () => {
    await wrapper.vm.setup()

    const bookmarks = await wrapper.findAll('task-record-review-card-stub')
    expect(wrapper.vm.taskRecordReviewIds).toHaveLength(5)
    expect(bookmarks).toHaveLength(5)
  })

  it('should display bookmarked items grouped by projects then by tasks', async () => {
    await wrapper.vm.setup()

    const project = await wrapper.findAll('.bookmarks-list__project')
    expect(project).toHaveLength(2)
    expect(project.at(0).find('h1').text()).toContain('Demeter')
    expect(project.at(1).find('h1').text()).toContain('Chronos')

    expect(wrapper.vm.taskIds).toHaveLength(2)
    expect(project.at(0).find('h2').text()).toContain('Shops')
    expect(project.at(1).find('h2').text()).toContain('Addresses')
  })

  it('should apply filters', async () => {
    await wrapper.setProps({ query: {'filter[project]': '2'} })
    await wrapper.vm.setup()

    let project = await wrapper.findAll('.bookmarks-list__project')
    expect(project).toHaveLength(1)
    expect(project.at(0).find('h1').text()).toContain('Demeter')
    expect(project.at(0).find('h2').text()).toContain('Shops')
    expect(project.at(0).findAll('task-record-review-card-stub')).toHaveLength(3)

    await wrapper.setProps({ query: {'filter[task]': '1'} })
    project = await wrapper.findAll('.bookmarks-list__project')
    expect(project).toHaveLength(1)
    expect(project.at(0).find('h1').text()).toContain('Chronos')
    expect(project.at(0).find('h2').text()).toContain('Addresses')
    expect(project.at(0).findAll('task-record-review-card-stub')).toHaveLength(2)
  })

  it('should show the message "No bookmarks" when list is empty', async () => {
    const element = wrapper.find('.bookmarks__no-items')
    expect(wrapper.vm.taskRecordReviewIds).toHaveLength(0)
    expect(element.exists()).toBeTruthy()
    expect(element.text()).toBe('No bookmarks')
  })
})
