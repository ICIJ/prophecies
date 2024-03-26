import { BButton } from 'bootstrap-vue'
import { createLocalVue, mount } from '@vue/test-utils'

import MultiselectButtons from '@/components/MultiselectButtons'

describe('MultiselectButtons', () => {
  let localVue
  let wrapper

  describe('a form with Correct/Incorrect/Unknown buttons', () => {
    beforeEach(() => {
      const options = [
        { id: 1, name: 'Correct' },
        { id: 2, name: 'Incorrect' },
        { id: 3, name: 'Unknown' }
      ]
      const propsData = { multiple: false, options, trackBy: 'id' }
      localVue = createLocalVue()
      localVue.component('BBtn', BButton)
      wrapper = mount(MultiselectButtons, { localVue, propsData })
    })

    it('should creates 4 buttons', () => {
      const buttons = wrapper.findAllComponents(BButton)
      expect(buttons).toHaveLength(4)
    })

    it('should select "Correct" when clicking on the second button', () => {
      const buttons = wrapper.findAllComponents(BButton)
      buttons.at(1).trigger('click')
      expect(wrapper.emitted().update[0][0]).toHaveLength(1)
      expect(wrapper.emitted().update[0][0]).toEqual(
        expect.arrayContaining([expect.objectContaining({ id: 1, name: 'Correct' })])
      )
    })

    it('should select not select anything when clicking on the first button', () => {
      const buttons = wrapper.findAllComponents(BButton)
      buttons.at(0).trigger('click')
      expect(wrapper.emitted().update[0][0]).toHaveLength(0)
    })

    it('should show the names in each button', () => {
      const buttons = wrapper.findAllComponents(BButton)
      expect(buttons.at(0).text()).toBe('all')
      expect(buttons.at(1).text()).toBe('Correct')
      expect(buttons.at(2).text()).toBe('Incorrect')
      expect(buttons.at(3).text()).toBe('Unknown')
    })

    it('should show use the `btn-outline-primary` on unselected buttons', () => {
      const buttons = wrapper.findAllComponents(BButton)
      expect(buttons.at(1).classes('btn-outline-primary')).toBeTruthy()
      expect(buttons.at(2).classes('btn-outline-primary')).toBeTruthy()
      expect(buttons.at(3).classes('btn-outline-primary')).toBeTruthy()
    })

    it('should show use the `btn-primary` on selected buttons', () => {
      const buttons = wrapper.findAllComponents(BButton)
      expect(buttons.at(0).classes('btn-primary')).toBeTruthy()
    })
  })

  describe('a form with Babka/Croissant/Muffin/Cookie buttons', () => {
    beforeEach(() => {
      const options = [
        { id: 1, name: 'Babka' },
        { id: 2, name: 'Croissant' },
        { id: 3, name: 'Muffin' },
        { id: 4, name: 'Cookie' }
      ]
      const value = [{ id: 2, name: 'Croissant' }]
      const propsData = { multiple: true, options, value }
      localVue = createLocalVue()
      localVue.component('BBtn', BButton)
      wrapper = mount(MultiselectButtons, { localVue, propsData })
    })

    it('should show the names in each button', () => {
      const buttons = wrapper.findAllComponents(BButton)
      expect(buttons.at(0).text()).toBe('all')
      expect(buttons.at(1).text()).toBe('Babka')
      expect(buttons.at(2).text()).toBe('Croissant')
      expect(buttons.at(3).text()).toBe('Muffin')
      expect(buttons.at(4).text()).toBe('Cookie')
    })

    it('should show use the `btn-outline-primary` on unselected buttons', () => {
      const buttons = wrapper.findAllComponents(BButton)
      expect(buttons.at(0).classes('btn-outline-primary')).toBeTruthy()
      expect(buttons.at(1).classes('btn-outline-primary')).toBeTruthy()
      expect(buttons.at(3).classes('btn-outline-primary')).toBeTruthy()
      expect(buttons.at(4).classes('btn-outline-primary')).toBeTruthy()
    })

    it('should show use the `btn-primary` on selected buttons', () => {
      const buttons = wrapper.findAllComponents(BButton)
      expect(buttons.at(2).classes('btn-primary')).toBeTruthy()
    })

    it('should select "Croissant" and "Cookie"', () => {
      const buttons = wrapper.findAllComponents(BButton)
      buttons.at(4).trigger('click')
      expect(wrapper.emitted().update[0][0]).toHaveLength(2)
      expect(wrapper.emitted().update[0][0]).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ id: 2, name: 'Croissant' }),
          expect.objectContaining({ id: 4, name: 'Cookie' })
        ])
      )
    })
  })
})
