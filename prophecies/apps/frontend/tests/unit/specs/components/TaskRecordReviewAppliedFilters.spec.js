import {createLocalVue, shallowMount} from '@vue/test-utils'
import {BButton} from 'bootstrap-vue'
import '@/store'
import Core from '@/core'
import ChoiceGroup from '@/models/ChoiceGroup'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import TaskRecordReviewAppliedFilters from '@/components/TaskRecordReviewAppliedFilters'

describe('TaskRecordReviewAppliedFilters', () => {
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
  })

  beforeEach(() => {
    const attachTo = createContainer()
    const localVue = createLocalVue()
    const routeFilters = {choice__in: '1,2', task_record__predicted_value__iregex: '(FRA|DZA)'}
    const propsData = {taskId: '1', routeFilters}
    // Configure the local vue with plugins
    const {store, wait} = Core.init(localVue).useAll()
    wrapper = shallowMount(TaskRecordReviewAppliedFilters, {attachTo, localVue, propsData, store, wait})
  })

  it('should return filters with selected option for the `predictedValues` filter', () => {
    const filters = wrapper.vm.filters
    expect(filters.predictedValues).toBeDefined()
    expect(filters.predictedValues.selected).toHaveLength(2)
  })

  it('should return filters with selected option for the `choices` filter', () => {
    const filters = wrapper.vm.filters
    expect(filters.choices).toBeDefined()
    expect(filters.choices.selected).toHaveLength(2)
  })

  it('should return filters without selected option for the `assignedTo` filter', () => {
    const filters = wrapper.vm.filters
    expect(filters.assignedTo).toBeDefined()
    expect(filters.assignedTo.selected).toHaveLength(0)
  })

  it('should create 4 buttons', () => {
    expect(wrapper.findAllComponents(BButton)).toHaveLength(4)
  })

  it('should create a button with "FRA" at position 0', () => {
    expect(wrapper.findAllComponents(BButton).at(0).text()).toBe('FRA')
  })

  it('should create a button with "Algeria (DZA)" at position 1', () => {
    expect(wrapper.findAllComponents(BButton).at(1).text()).toBe('Algeria (DZA)')
  })

  it('should create a button with "Correct" at position 2', () => {
    expect(wrapper.findAllComponents(BButton).at(2).text()).toBe('Correct')
  })

  it('should create a button with "Incorrect" at position 3', () => {
    expect(wrapper.findAllComponents(BButton).at(3).text()).toBe('Incorrect')
  })

  it('should emit an `update:routeFilters` event on click on btn 0 and remove "FRA"', () => {
    wrapper.findAllComponents(BButton).at(0).trigger('click')
    const event = wrapper.emitted()['update:routeFilters']
    expect(event).toBeTruthy()
    expect(event[0][0]['filter[task_record__predicted_value__iregex]']).toBe('(DZA)')
  })

  it('should emit an `update:routeFilters` event on click on btn 1 and remove "DZA"', () => {
    wrapper.findAllComponents(BButton).at(1).trigger('click')
    const event = wrapper.emitted()['update:routeFilters']
    expect(event).toBeTruthy()
    expect(event[0][0]['filter[task_record__predicted_value__iregex]']).toBe('(FRA)')
  })

  it('should emit an `update:routeFilters` event on click on btn 0 and remove choice 1', () => {
    wrapper.findAllComponents(BButton).at(2).trigger('click')
    const event = wrapper.emitted()['update:routeFilters']
    expect(event).toBeTruthy()
    expect(event[0][0]['filter[choice__in]']).toBe('2')
  })

  it('should emit an `update:routeFilters` event on click on btn 1 and remove choice 2', () => {
    wrapper.findAllComponents(BButton).at(3).trigger('click')
    const event = wrapper.emitted()['update:routeFilters']
    expect(event).toBeTruthy()
    expect(event[0][0]['filter[choice__in]']).toBe('1')
  })
})
