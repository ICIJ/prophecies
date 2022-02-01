import {createLocalVue, shallowMount} from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import TaskRecordReview from '@/models/TaskRecordReview'
import Task from '@/models/Task'
import Bookmarks from '@/views/Bookmarks'
import User from '@/models/User'
import ChoiceGroup from '@/models/ChoiceGroup'


describe('Bookmarks', () => {
  let wrapper

  beforeAll(async () => {
    await User.api().me()
    await TaskRecordReview.api().get()
    await Task.api().get()
    await ChoiceGroup.api().get()
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
    await wrapper.destroy()
  })

  it('show the message "No bookmarks"', async () => {
    const element = wrapper.find('.bookmarks__no-items')
    expect(wrapper.vm.taskRecordReviewIds).toHaveLength(0)
    expect(element.exists()).toBeTruthy()
    expect(element.text()).toBe('No bookmarks')
  })
})
