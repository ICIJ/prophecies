import '@/store'

import { createLocalVue, shallowMount } from '@vue/test-utils'

import Core from '@/core'
import CinematicView from '@/components/CinematicView'
import TaskRecordReview from '@/models/TaskRecordReview'
import Task from '@/models/Task'
import User from '@/models/User'

describe('CinematicView', () => {
  let wrapper

  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  beforeEach(async () => {
    await User.api().me()
    await Task.api().get()
    await TaskRecordReview.api().get()
    const attachTo = createContainer()
    const localVue = createLocalVue()
    const { wait, store } = Core.init(localVue).useAll()
    const taskRecordReviewIds = TaskRecordReview.all().map(({ id }) => id)
    const pageNumber = 1
    const totalRows = 10
    const perPage = 5
    const propsData = { pageNumber, perPage, taskRecordReviewIds, totalRows }
    wrapper = shallowMount(CinematicView, { attachTo, localVue, propsData, wait, store })
  })

  it('should have five reviews', () => {
    expect(wrapper.vm.taskRecordReviews.count()).toBe(6)
  })

  it('should have two pending reviews', () => {
    expect(wrapper.vm.pendingTaskRecordReviews.count()).toBe(2)
  })

  it('should be the first page', () => {
    expect(wrapper.vm.isFirstPage).toBeTruthy()
  })

  it('should not be the last page', () => {
    expect(wrapper.vm.isLastPage).toBeFalsy()
  })

  it('should show the first pending review by default', () => {
    expect(wrapper.vm.id).toBe(wrapper.vm.pendingTaskRecordReviews.first().id)
  })

  it('should show a different review after clicking on next', async () => {
    await wrapper.find('.cinematic-view__nav__next').trigger('click')
    expect(wrapper.vm.id).not.toBe(wrapper.vm.pendingTaskRecordReviews.first().id)
  })

  it('should not go to the previous page after clicking on previous from the first review', async () => {
    await wrapper.setData({ id: wrapper.vm.taskRecordReviews.first().id })
    await wrapper.find('.cinematic-view__nav__previous').trigger('click')
    expect(wrapper.vm.id).toBe(wrapper.vm.taskRecordReviews.first().id)
    expect(wrapper.emitted().previousPage).toBeFalsy()
  })

  it('should go to the next page after clicking on next from the last review', async () => {
    await wrapper.setData({ id: wrapper.vm.taskRecordReviews.last().id })
    await wrapper.find('.cinematic-view__nav__next').trigger('click')
    expect(wrapper.emitted().nextPage).toBeTruthy()
  })

  it('should "slide forward" after clicking on next', async () => {
    await wrapper.setData({ id: wrapper.vm.taskRecordReviews.first().id })
    await wrapper.find('.cinematic-view__nav__next').trigger('click')
    expect(wrapper.vm.transition).toBe('slide-forward')
  })

  it('should "slide backward" after clicking on previous', async () => {
    await wrapper.setData({ id: wrapper.vm.taskRecordReviews.last().id })
    await wrapper.find('.cinematic-view__nav__previous').trigger('click')
    expect(wrapper.vm.transition).toBe('slide-backward')
  })

  it('should "slide forward" when going to the next page', async () => {
    await wrapper.setData({ id: wrapper.vm.taskRecordReviews.last().id })
    await wrapper.setProps({ pageNumber: 2, taskRecordReviewIds: ['100'] })
    expect(wrapper.vm.transition).toBe('slide-forward')
  })

  it('should "slide backward" when going to the previous page', async () => {
    await wrapper.setProps({ pageNumber: 2, taskRecordReviewIds: ['100'] })
    const taskRecordReviewIds = TaskRecordReview.all().map(({ id }) => id)
    await wrapper.setProps({ pageNumber: 1, taskRecordReviewIds })
    expect(wrapper.vm.transition).toBe('slide-backward')
  })

  it('should be on index 1 with the first review', async () => {
    await wrapper.setData({ id: wrapper.vm.taskRecordReviews.first().id })
    expect(wrapper.vm.progressIndex).toBe(1)
  })

  it('should be on index 5 with the last review', async () => {
    await wrapper.setData({ id: wrapper.vm.taskRecordReviews.last().id })
    expect(wrapper.vm.progressIndex).toBe(6)
  })

  it('should be on the first review of the next page', async () => {
    await wrapper.setProps({ pageNumber: 2, taskRecordReviewIds: ['100'] })
    expect(wrapper.vm.id).toBe('100')
  })

  it('should be on index 6 with the first review of the next page', async () => {
    await wrapper.setProps({ pageNumber: 2, taskRecordReviewIds: ['100'] })
    expect(wrapper.vm.progressIndex).toBe(6)
  })

  it('should not be able to go to a third page', async () => {
    await wrapper.setProps({ pageNumber: 2, taskRecordReviewIds: ['100'] })
    await wrapper.find('.cinematic-view__nav__next').trigger('click')
    expect(wrapper.emitted().nextPage).toBeFalsy()
  })
})
