import { createLocalVue, mount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import ChoiceGroup from '@/models/ChoiceGroup'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import User from '@/models/User'
import TaskRecordReviewHistory from '@/components/TaskRecordReviewHistory'

describe('TaskRecordReviewHistory', () => {
  let wrapper

  function createContainer () {
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

  beforeEach(() => {
    const attachTo = createContainer()
    const localVue = createLocalVue()
    const propsData = { taskRecordReviewId: '38' }
    // Configure the local vue with plugins
    const { store, router,wait } = Core.init(localVue).useAll()
    wrapper = mount(TaskRecordReviewHistory, { attachTo, localVue, propsData, store, router, wait })
  })

  it('should find the right task record review', () => {
    expect(wrapper.vm.taskRecordReview.status).toBe('DONE')
  })

  it('should find the a task record review with a checker', () => {
    expect(wrapper.vm.taskRecordReview.checker.username).toBe('django')
  })

  it('should find the a task record review with an history', () => {
    expect(wrapper.vm.history).toHaveLength(1)
  })

  it('should find the a task record review with an history and its checkers', () => {
    expect(wrapper.vm.history[0].checker.username).toBe('django')
  })

  it('should be me', () => {
    expect(wrapper.vm.isMe({ id: '2' })).toBeTruthy()
  })

  it('should not be me', () => {
    expect(wrapper.vm.isMe({ id: '3' })).toBeFalsy()
  })

  it('should only show the first letter of the status', () => {
    const firstCheckerBadge = wrapper.find('.task-record-review-history__checker__choice__badge')
    expect(firstCheckerBadge.text()).toBe('Unkown')
    const firstCheckerBadgeEnd = wrapper.find('.task-record-review-history__checker__choice__badge .sr-only')
    expect(firstCheckerBadgeEnd.text()).toBe('nkown')
  })

  it('should show "you" next to the current checker name', () => {
    const firstCheckerName = wrapper.find('.task-record-review-history__checker__name')
    expect(firstCheckerName.text()).toMatch(/Django\s+\(you\)/)
  })

  it('should emit `task-record-review-history__checker__note` to emit an event on click', () => {
    const noteBtn = wrapper.find('.task-record-review-history__checker__note')
    noteBtn.trigger('click')
    expect(wrapper.emitted()['toggle-notes']).toBeTruthy()
    expect(wrapper.emitted()['toggle-notes'][0][0]).toBe(wrapper.vm.taskRecordReview.id)
  })

  it('should find the name of the alternative value', () => {
    const { alternativeValueName } = wrapper.vm.$options.filters
    expect(alternativeValueName('DZA')).toBe('Algeria (DZA)')
  })

  it('should not find the name of the alternative value and return the value instead', () => {
    const { alternativeValueName } = wrapper.vm.$options.filters
    expect(alternativeValueName('FRA')).toBe('"FRA"')
  })
})
