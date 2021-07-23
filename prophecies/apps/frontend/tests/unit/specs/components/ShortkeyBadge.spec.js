import { createLocalVue, mount } from '@vue/test-utils'
import ShortkeyBadge from '@/components/ShortkeyBadge'

describe('AppHeader', () => {
  let localVue
  let wrapper

  beforeEach(() => {
    localVue = createLocalVue()
    wrapper = mount(ShortkeyBadge, { localVue })
  })

  it('should read keys from an array', async () => {
    await wrapper.setProps({ value: ['Ctrl', 'L'] })
    expect(wrapper.text()).toBe('Ctrl + L')
  })

  it('should read keys from an array with sub key', async () => {
    await wrapper.setProps({ value: ['Ctrl', 'L+S+D'] })
    expect(wrapper.text()).toBe('Ctrl + L + S + D')
  })

  it('should read keys from a string', async () => {
    await wrapper.setProps({ value: 'Ctrl + L' })
    expect(wrapper.text()).toBe('Ctrl + L')
  })

  it('should read keys from a string and fix spacing', async () => {
    await wrapper.setProps({ value: 'Ctrl+L' })
    expect(wrapper.text()).toBe('Ctrl + L')
  })

  it('should fix case for single char key', async () => {
    await wrapper.setProps({ value: 'l' })
    expect(wrapper.text()).toBe('L')
  })

  it('should convert the "meta" keyword to the right system key', async () => {
    await wrapper.setProps({ value: 'l' })
    expect(wrapper.text()).toBe('L')
  })
})
