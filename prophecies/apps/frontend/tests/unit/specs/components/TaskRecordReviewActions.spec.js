import { createLocalVue, shallowMount, mount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import User from '@/models/User'
import ChoiceGroup from '@/models/ChoiceGroup'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import TaskRecordReviewActions from '@/components/TaskRecordReviewActions'

describe('TaskRecordReviewActions', () => {
  let wrapper

  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }
  beforeAll(async () => {
    await ChoiceGroup.api().get()
    await Task.api().get()
    await TaskRecordReview.api().get()
    await User.api().me()
  })

  beforeEach(async () => {
    const attachTo = createContainer()
    const localVue = createLocalVue()
    const propsData = { taskId: '1', taskRecordReviewId: '38' }
    // Configure the local vue with plugins
    const { store, wait } = Core.init(localVue).useAll()
    wrapper = shallowMount(TaskRecordReviewActions, { attachTo, localVue, propsData, store, wait })
  })

  it('should prevent user from locking a record when the task is NOT open', () => {
    const taskNotOpened = wrapper.find('.task-record-review-actions__task_not_open')
    expect(taskNotOpened.exists()).toBe(true)
  })
  
  it('should prevent user from locking a record when the task is OPEN', async () => {
    const propsData = { taskId: '2', taskRecordReviewId: '25' }
    await wrapper.setProps(propsData)
    const taskNotOpened = wrapper.find('.task-record-review-actions__task_not_open')
    expect(taskNotOpened.exists()).toBe(false)
  })
})
