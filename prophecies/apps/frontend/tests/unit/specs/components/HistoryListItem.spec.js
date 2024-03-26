import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import HistoryListItem, { ITEM_TYPES } from '@/components/HistoryListItem'

describe('HistoryListItem', () => {
  let wrapper

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const { store, i18n } = Core.init(localVue).useAll()
    const propsData = {
      type: ITEM_TYPES.MENTIONED_USER,
      timestamp: '2021-10-14T15:10:53.364880Z',
      creator: {
        id: '1',
        username: 'olivia',
        displayName: 'Olivia',
        isMe: true
      },
      value: {
        id: '1',
        username: 'olivia',
        displayName: 'Olivia',
        isMe: true
      },
      projectName: 'Chronos',
      taskName: 'Addresses',
      link: '#/task-record-reviews/1/101?highlightNote=true'
    }
    wrapper = await shallowMount(HistoryListItem, {
      localVue,
      store,
      propsData,
      i18n
    })
  })

  it('should display the timestamp as iso date', () => {
    const dateColumn = wrapper.find('.history-list-item__date-column')
    expect(dateColumn.text()).toBe('Thu 14, Oct 2021 - 3:10pm')
  })

  it('should display the category format  "Task | project"', async () => {
    expect(wrapper.vm.category).toBe('Addresses | Chronos')
  })

  it('should display the category format  "General | project" when no task is set', async () => {
    await wrapper.setProps({ taskName: null })
    expect(wrapper.vm.category).toBe('General | Chronos')
  })

  it('should display the category format  "General" when no project is set', async () => {
    await wrapper.setProps({ projectName: null })
    expect(wrapper.vm.category).toBe('General')
  })

  it('should display "you" when the event concerns me', async () => {
    let elem = wrapper.find('.history-list-item__content-column')
    expect(elem.text()).toBe('You mentioned you (@olivia) in a note')
    await wrapper.setProps({
      value: {
        id: '1',
        displayName: 'Olivia',
        username: 'olivia',
        isMe: false
      }
    })

    elem = wrapper.find('.history-list-item__content-column')
    expect(elem.text()).toBe('You mentioned Olivia (@olivia) in a note')
    await wrapper.setProps({
      creator: {
        id: '1',
        displayName: 'Olivia',
        username: 'olivia',
        isMe: false
      }
    })

    elem = wrapper.find('.history-list-item__content-column')
    expect(elem.text()).toBe('Olivia mentioned Olivia (@olivia) in a note')
  })

  it('should display a mention text for a user mentioned event', async () => {
    const elem = wrapper.find('.history-list-item__content-column')
    expect(elem.text()).toBe('You mentioned you (@olivia) in a note')
  })

  it('should display a tip text for a tip event', async () => {
    const propsData = {
      type: ITEM_TYPES.TIP,
      timestamp: '2021-10-14T15:10:53.364880Z',
      creator: {
        id: '1',
        username: 'olivia',
        displayName: 'Olivia',
        isMe: true
      },
      value: 'Bonjour hello',
      projectName: 'Chronos',
      taskName: 'Addresses',
      link: '#/tips/1'
    }
    await wrapper.setProps(propsData)
    const elem = wrapper.find('.history-list-item__content-column')
    expect(elem.text()).toBe('You added a new tip: "Bonjour hello"')
  })

  it('should display a closed task text for a closed task event', async () => {
    const propsData = {
      type: ITEM_TYPES.CLOSED_TASK,
      timestamp: '2021-10-14T15:10:53.364880Z',
      creator: {
        id: '1',
        username: 'olivia',
        displayName: 'Olivia',
        isMe: true
      },
      projectName: 'Chronos',
      taskName: 'Addresses',
      link: '#/tips/1'
    }
    await wrapper.setProps(propsData)
    const elem = wrapper.find('.history-list-item__content-column')
    expect(elem.text()).toBe('You closed the task')
  })
})
