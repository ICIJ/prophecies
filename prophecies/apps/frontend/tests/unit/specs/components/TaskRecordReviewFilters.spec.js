import { createLocalVue, shallowMount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import ChoiceGroup from '@/models/ChoiceGroup'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import TaskRecordReviewFilters from '@/components/TaskRecordReviewFilters'

describe('TaskRecordReviewFilters', () => {
  let wrapper

  beforeAll(async () => {
    await ChoiceGroup.api().get()
    await Task.api().get()
    await TaskRecordReview.api().get()
  })

  describe('without route filters', () => {
    beforeEach(() => {
      const localVue = createLocalVue()
      const propsData = { taskId: '1' }
      // Configure the local vue with plugins
      const { store, wait } = Core.init(localVue).useAll()
      wrapper = shallowMount(TaskRecordReviewFilters, { localVue, propsData, store, wait })
    })

    it('should find the right task', () => {
      expect(wrapper.vm.task.name).toBe('Addresses')
    })

    it('should find the a task with a list of checkers', () => {
      expect(wrapper.vm.task.checkers).toHaveLength(1)
      expect(wrapper.vm.task.checkers[0].username).toBe('django')
    })

    it('should find the a task with a choice group', () => {
      expect(wrapper.vm.task.choiceGroup.name).toBe('Is it correct?')
    })

    it('should find the a task with a choice group with its choices', () => {
      expect(wrapper.vm.task.choiceGroup.choices).toHaveLength(3)
    })

    it('should find the a task with a choice group with its alternative values', () => {
      expect(wrapper.vm.task.choiceGroup.alternativeValues).toHaveLength(2)
    })

    it('should have an object describing filters, including predictedValues', () => {
      expect(wrapper.vm.filters.predictedValues).toBeDefined()
      expect(wrapper.vm.filters.predictedValues.param).toBe('task_record__predicted_value__iregex')
      expect(wrapper.vm.filters.predictedValues.options).toHaveLength(2)
    })

    it('should have an object describing filters, including assignedTo', () => {
      expect(wrapper.vm.filters.assignedTo).toBeDefined()
      expect(wrapper.vm.filters.assignedTo.param).toBe('task_record__reviews__checker__in')
      expect(wrapper.vm.filters.assignedTo.options).toHaveLength(1)
    })

    it('should have an object describing filters, including reviewedBy', () => {
      expect(wrapper.vm.filters.reviewedBy).toBeDefined()
      expect(wrapper.vm.filters.reviewedBy.options).toHaveLength(1)
    })

    it('should have an object describing filters, including choices', () => {
      expect(wrapper.vm.filters.choices).toBeDefined()
      expect(wrapper.vm.filters.choices.param).toBe('choice__in')
      expect(wrapper.vm.filters.choices.options).toHaveLength(4)
    })

    it('should have add an arbitrary value to the `predictedValues` filter', () => {
      wrapper.vm.addArbitraryPredictedValue('foo')
      expect(wrapper.vm.selected.predictedValues).toHaveLength(1)
      wrapper.vm.addArbitraryPredictedValue('bar')
      expect(wrapper.vm.selected.predictedValues).toHaveLength(2)
    })

    it('should have add an arbitrary value to the `predictedValues` filter with the correct attributes', () => {
      wrapper.vm.addArbitraryPredictedValue('foo')
      expect(wrapper.vm.selected.predictedValues[0].id).toBeDefined()
      expect(wrapper.vm.selected.predictedValues[0].value).toBe('foo')
      expect(wrapper.vm.selected.predictedValues[0].name).toBe('foo')
    })

    it('should return filters as query params for the `predictedValues` filter', () => {
      wrapper.vm.addArbitraryPredictedValue('foo')
      wrapper.vm.selected.predictedValues.push({ id: '100', value: 'bar' })
      const queryParams = wrapper.vm.filtersAsQueryParams
      expect(queryParams['filter[task_record__predicted_value__iregex]']).toBeDefined()
      expect(queryParams['filter[task_record__predicted_value__iregex]']).toBe('(foo|bar)')
    })

    it('should return filters as query params for the `choices` filter', () => {
      wrapper.vm.selected.choices.push({ id: '1', value: 'foo' })
      wrapper.vm.selected.choices.push({ id: '2', value: 'bar' })
      const queryParams = wrapper.vm.filtersAsQueryParams
      expect(queryParams['filter[choice__in]']).toBeDefined()
      expect(queryParams['filter[choice__in]']).toBe('1,2')
    })
  })

  describe('with route filters', () => {
    beforeEach(() => {
      const localVue = createLocalVue()
      const routeFilters = { choice__in: '1,2', task_record__predicted_value__iregex: '(FRA|DZA)' }
      const propsData = { taskId: '1', routeFilters }
      // Configure the local vue with plugins
      const { store, wait } = Core.init(localVue).useAll()
      wrapper = shallowMount(TaskRecordReviewFilters, { localVue, propsData, store, wait })
    })

    it('should return filters as query params for the `predictedValues` filter', () => {
      const queryParams = wrapper.vm.filtersAsQueryParams
      expect(queryParams['filter[task_record__predicted_value__iregex]']).toBeDefined()
      expect(queryParams['filter[task_record__predicted_value__iregex]']).toBe('(FRA|DZA)')
    })

    it('should return filters as query params for the `choices` filter', () => {
      const queryParams = wrapper.vm.filtersAsQueryParams
      expect(queryParams['filter[choice__in]']).toBeDefined()
      expect(queryParams['filter[choice__in]']).toBe('1,2')
    })

    it('should convert "FRA" to an arbitrary predicted value', () => {
      const selected = wrapper.vm.selected.predictedValues
      expect(selected[0].id.split('-').shift()).toBe('arbitrary')
      expect(selected[0].value).toBe('FRA')
      expect(selected[0].name).toBe('FRA')
    })

    it('should convert "DZA" to an existing predicted value option', () => {
      const selected = wrapper.vm.selected.predictedValues
      expect(selected[1].id).toBe('11')
      expect(selected[1].value).toBe('DZA')
      expect(selected[1].name).toBe('Algeria (DZA)')
    })
  })
})
