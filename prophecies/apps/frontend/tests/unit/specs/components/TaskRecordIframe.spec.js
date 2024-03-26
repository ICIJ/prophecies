import { createLocalVue, mount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import TaskRecord from '@/models/TaskRecord'
import TaskRecordIframe from '@/components/TaskRecordIframe'

describe('TaskRecordIframe', () => {
  let wrapper

  beforeAll(async () => {
    TaskRecord.insert({
      data: { id: '1000', embeddableLink: 'https://foo' }
    })
  })

  beforeEach(() => {
    const localVue = createLocalVue()
    const propsData = { taskRecordId: '1000' }
    // Configure the local vue with plugins
    const { i18n, store, wait } = Core.init(localVue).useAll()
    wrapper = mount(TaskRecordIframe, { localVue, propsData, i18n, store, wait })
  })

  it('contains an iframe with the correct link', () => {
    const iframe = wrapper.find('iframe')
    expect(iframe.attributes('src')).toBe('https://foo')
  })

  it('contains an iframe with the blank link if `hidden` is true', async () => {
    await wrapper.setProps({ hidden: true })
    const iframe = wrapper.find('iframe')
    expect(iframe.attributes('src')).toBe('about:blank')
  })

  it('doesnt contain an expand button by default', () => {
    const btn = wrapper.find('.task-record-iframe__expand')
    expect(btn.exists()).toBeFalsy()
  })

  it('contains an expand button if `expand` is true', async () => {
    await wrapper.setProps({ expand: true })
    const btn = wrapper.find('.task-record-iframe__expand')
    expect(btn.exists()).toBeTruthy()
  })
})
