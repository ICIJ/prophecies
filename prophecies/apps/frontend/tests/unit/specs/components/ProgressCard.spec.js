import { createLocalVue, mount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import ProgressCard from '@/components/ProgressCard'
import { server, rest } from '../../mocks/server'

describe('ProgressCard', () => {
  let wrapper

  beforeAll(async () => {
    await Task.api().get()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const core = Core.init(localVue).useAll()
    const { i18n, router } = core
    const stubs = ['router-link']
    wrapper = mount(ProgressCard, { localVue, i18n, stubs, router })
  })

  it('should show 4 progress items', () => {
    const elements = wrapper.findAll('.progress-card__items__item')
    expect(elements).toHaveLength(4)
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
    expect(element.text()).toBe('47%')
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
    expect(element.text()).toBe('53%')
  })

  it('should show the link to the stats', () => {
    const element = wrapper.find('.progress-card__stats-link')
    expect(element.text()).toBe('More progress')
  })

  describe('No task opened', () => {
    beforeEach(async () => {
      Task.deleteAll()
      server.use(rest.get('/api/v1/tasks', (req, res, ctx) => {
        return res.once(ctx.json({
          data: [
            {
              type: 'Task',
              id: '1',
              attributes: {
                status: 'CLOSED'
              },
              relationships: {
                choiceGroup: {
                  data: {
                    type: 'ChoiceGroup',
                    id: '1'
                  }
                },
                project: {
                  data: {
                    type: 'Project',
                    id: '1'
                  }
                },
                checkers: {
                  meta: {
                    count: 1
                  },
                  data: [
                    {
                      type: 'User',
                      id: '2'
                    }
                  ]
                }
              },
              links: {
                self: 'http://localhost/api/v1/tasks/1/'
              }
            }
          ]
        }))
      }))

      await Task.api().get()
    })
    afterEach(() => {
      Task.deleteAll()
      server.resetHandlers()
    })
    it('show the message "No open tasks"', () => {
      const element = wrapper.find('.progress-card__no-items')
      expect(wrapper.vm.tasks).toHaveLength(0)
      expect(element.exists()).toBeTruthy()
      expect(element.text()).toBe('No open tasks')
    })
  })
})
