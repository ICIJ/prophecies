import { createLocalVue, mount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import ProgressCard from '@/components/ProgressCard'

describe('ProgressCard', () => {
  let wrapper

  beforeAll(async () => {
    await Task.api().get()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    Core.init(localVue).useAll()
    wrapper = mount(ProgressCard, { localVue })
  })

  it('should show 3 progress items', () => {
    const elements = wrapper.findAll('.progress-card__items__item')
    expect(elements).toHaveLength(3)
  })

  it('should show the overall progress', () => {
    const element = wrapper.findAll('.progress-card__items__item').at(0)
    expect(element.classes('progress-card__items__item--mean')).toBe(true)
  })

  it('should show the "Adresses" task second', () => {
    const element = wrapper.findAll('.progress-card__items__item__name').at(1)
    expect(element.text()).toBe('Addresses')
  })

  it('should show the "Shop" task third', () => {
    const element = wrapper.findAll('.progress-card__items__item__name').at(2)
    expect(element.text()).toBe('Shops')
  })

  it('should show a 50% progess for the user on task "Adresses"', async () => {
    await wrapper.setData({ team: false })
    const element = wrapper.findAll('.progress-card__items__item__value').at(1)
    expect(element.text()).toBe('50%')
  })

  it('should show a 45% progess for the user on task "Shop"', async () => {
    await wrapper.setData({ team: false })
    const element = wrapper.findAll('.progress-card__items__item__value').at(2)
    expect(element.text()).toBe('45%')
  })

  it('should show the average progess for the user', async () => {
    await wrapper.setData({ team: false })
    const element = wrapper.findAll('.progress-card__items__item__value').at(0)
    expect(element.text()).toBe('48%')
  })

  it('should show a 40% progess for the team on task "Adresses"', () => {
    const element = wrapper.findAll('.progress-card__items__item__value').at(1)
    expect(element.text()).toBe('40%')
  })

  it('should show a 60% progess for the team on task "Shop"', () => {
    const element = wrapper.findAll('.progress-card__items__item__value').at(2)
    expect(element.text()).toBe('60%')
  })

  it('should show the average progess for the team', () => {
    const element = wrapper.findAll('.progress-card__items__item__value').at(0)
    expect(element.text()).toBe('50%')
  })
})
