import { find } from 'lodash'
import { createLocalVue, mount } from '@vue/test-utils'
import AppSearchForm from '@/components/AppSearchForm'
import Core from '@/core'
import Task from '@/models/Task'

describe('AppSearchForm', () => {
  describe('with 2 tasks', () => {
    let wrapper

    function createContainer () {
      const div = document.createElement('div')
      document.body.appendChild(div)
      return div
    }

    beforeAll(async () => {
      await Task.api().get()
    })

    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const core = Core.init(localVue).useAll()
      const { i18n, store, wait } = core
      const stubs = ['router-link', 'app-waiter']
      await core.configure()
      // Finally, instantiate the component
      wrapper = mount(AppSearchForm, { attachTo, i18n, localVue, stubs, store, wait })
    })

    afterEach(async () => {
      // Prevent a Vue warning in the next tick when the parentNode doesnt exist:
      // > TypeError: Cannot read property 'createElement' of null
      // @see https://stackoverflow.com/a/62262333
      wrapper.destroy()
    })

    it('should search tips', async () => {
      const spy = jest.spyOn(wrapper.vm, 'searchTips')
      await wrapper.vm.search('foo')
      expect(spy).toBeCalledWith('foo', expect.anything())
      expect(spy).toHaveBeenCalledTimes(1)
    })

    it('should not search tips twice because of throttle', async () => {
      const spy = jest.spyOn(wrapper.vm, 'searchTips')
      await wrapper.vm.searchWithThrottle('foo')
      expect(spy).toBeCalledWith('foo', expect.anything())
      expect(spy).toHaveBeenCalledTimes(1)
      await wrapper.vm.searchWithThrottle('bar')
      expect(spy).not.toBeCalledWith('bar', expect.anything())
      expect(spy).toHaveBeenCalledTimes(1)
    })

    it('should search reviews for tasks (with at least one record) 1, 3 and 4', async () => {
      const spy = jest.spyOn(wrapper.vm, 'searchTaskRecordReview')
      await wrapper.vm.search('foo')
      expect(spy).toHaveBeenCalledTimes(3)
      expect(spy).toBeCalledWith('foo', expect.anything(), '1')
      expect(spy).toBeCalledWith('foo', expect.anything(), '3')
      expect(spy).toBeCalledWith('foo', expect.anything(), '4')
    })

    it('should return a queryset of 2 tips and 15 reviews', async () => {
      await wrapper.setData({ query: 'buz' })
      await wrapper.vm.search('buz')
      expect(wrapper.vm.queryset).toHaveLength(17)
      expect(wrapper.vm.queryset).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ id: '3', type: 'Tip' }),
          expect.objectContaining({ id: '4', type: 'Tip' }),
          expect.objectContaining({ id: '36', type: 'TaskRecordReview' }),
          expect.objectContaining({ id: '37', type: 'TaskRecordReview' }),
          expect.objectContaining({ id: '38', type: 'TaskRecordReview' }),
          expect.objectContaining({ id: '25', type: 'TaskRecordReview' }),
          expect.objectContaining({ id: '24', type: 'TaskRecordReview' }),
          expect.objectContaining({ id: '36', type: 'TaskRecordReview' }),
          expect.objectContaining({ id: '37', type: 'TaskRecordReview' }),
          expect.objectContaining({ id: '38', type: 'TaskRecordReview' }),
          expect.objectContaining({ id: '25', type: 'TaskRecordReview' }),
          expect.objectContaining({ id: '24', type: 'TaskRecordReview' }),
        ])
      )
    })

    it('should deactivate item after a search', async () => {
      await wrapper.setData({ activeItem: 1 })
      await wrapper.setData({ query: 'buz' })
      await wrapper.vm.search('buz')
      expect(wrapper.vm.activeItem).toBe(-1)
    })

    it('should not be able to activate item bellow -1', async () => {
      await wrapper.setData({ activeItem: -1 })
      wrapper.vm.activatePreviousItem()
      expect(wrapper.vm.activeItem).toBe(-1)
    })

    it('should not be able to activate item above the current queryset size', async () => {
      await wrapper.setData({ query: 'buz' })
      await wrapper.vm.search('buz')
      await wrapper.setData({ activeItem: 4 })
      wrapper.vm.activateNextItem()
      expect(wrapper.vm.activeItem).toBe(4)
    })

    it('should not be able to activate previous item when no queryset', async () => {
      wrapper.vm.activatePreviousItem()
      expect(wrapper.vm.activeItem).toBe(-1)
    })

    it('should not be able to activate next item when no queryset', async () => {
      wrapper.vm.activateNextItem()
      expect(wrapper.vm.activeItem).toBe(-1)
    })

    it('should have no active queryset before search', async () => {
      expect(wrapper.vm.activeQuerysetId).toBeNull()
      expect(wrapper.vm.activeQueryset).toHaveLength(0)
    })

    it('should focus on the search input when reaching item -1', async () => {
      await wrapper.setData({ query: 'buz' })
      await wrapper.vm.search('buz')
      wrapper.vm.activateNextItem()
      wrapper.vm.activatePreviousItem()
      await wrapper.vm.$nextTick()
      const input = wrapper.find(wrapper.vm.searchInputSelector)
      expect(input.element).toBe(document.activeElement)
    })

    it('should activate the queryset with more results by default', async () => {
      await wrapper.setData({ query: 'buz' })
      await wrapper.vm.search('buz')
      const querysetId = wrapper.vm.activeQuerysetId
      const firstQuerysetMatch = find(wrapper.vm.queryset, { querysetId })
      expect(firstQuerysetMatch.type).toBe('TaskRecordReview')
      expect(wrapper.vm.activeQueryset).toHaveLength(5)
    })

    it('should count tips 2 tips and 3 reviews for each tasks having at least one record', async () => {
      await wrapper.setData({ query: 'buz' })
      await wrapper.vm.search('buz')
      expect(wrapper.vm.counts).toHaveLength(4)
      expect(wrapper.vm.counts).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ count: 2, querysetId: expect.anything() }),
          expect.objectContaining({ count: 3, querysetId: expect.anything() }),
          expect.objectContaining({ count: 3, querysetId: expect.anything() }),
          expect.objectContaining({ count: 3, querysetId: expect.anything() })
        ])
      )
    })
  })

  describe('without tasks', () => {
    let wrapper

    beforeEach(async () => {
      Task.deleteAll()
      const localVue = createLocalVue()
      const core = Core.init(localVue).useAll()
      const { i18n, store, wait } = core
      const stubs = ['router-link', 'app-waiter']
      await core.configure()
      // Finally, instantiate the component
      wrapper = mount(AppSearchForm, { i18n, localVue, stubs, store, wait })
    })

    afterEach(async () => {
      // Prevent a Vue warning in the next tick when the parentNode doesnt exist:
      // > TypeError: Cannot read property 'createElement' of null
      // @see https://stackoverflow.com/a/62262333
      wrapper.destroy()
    })

    it('should not search reviews when no task in the store', async () => {
      const spy = jest.spyOn(wrapper.vm, 'searchTaskRecordReview')
      await wrapper.vm.search('baz')
      expect(spy).toHaveBeenCalledTimes(0)
    })

    it('should return a queryset of 2 tips', async () => {
      await wrapper.setData({ query: 'foo' })
      await wrapper.vm.search('foo')
      expect(wrapper.vm.queryset).toHaveLength(2)
      expect(wrapper.vm.queryset).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ id: '3', type: 'Tip' }),
          expect.objectContaining({ id: '4', type: 'Tip' })
        ])
      )
    })
  })
})
