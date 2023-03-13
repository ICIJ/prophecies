import {createLocalVue, mount} from '@vue/test-utils'
import ShortkeyBadge from '@/components/ShortkeyBadge'

describe('ShortkeyBadge', () => {
  let localVue
  let wrapper
  let userAgentGetter

  beforeAll(() => {
    userAgentGetter = jest.spyOn(window.navigator, 'userAgent', 'get')
  })

  beforeEach(() => {
    localVue = createLocalVue()
    wrapper = mount(ShortkeyBadge, {localVue})
  })

  afterAll(() => {
    jest.restoreAllMocks()
  })

  it('should read keys from an array', async () => {
    await wrapper.setProps({value: ['Ctrl', 'L']})
    expect(wrapper.text()).toBe('Ctrl + L')
  })

  it('should read keys from an array with sub key', async () => {
    await wrapper.setProps({value: ['Ctrl', 'L+S+D']})
    expect(wrapper.text()).toBe('Ctrl + L + S + D')
  })

  it('should read keys from a string', async () => {
    await wrapper.setProps({value: 'Ctrl + L'})
    expect(wrapper.text()).toBe('Ctrl + L')
  })

  it('should read keys from a string and fix spacing', async () => {
    await wrapper.setProps({value: 'Ctrl+L'})
    expect(wrapper.text()).toBe('Ctrl + L')
  })

  it('should fix case for single char key', async () => {
    await wrapper.setProps({value: 'l'})
    expect(wrapper.text()).toBe('L')
  })

  it('should convert the "meta" keyword to "⌘" on Mac', async () => {
    userAgentGetter.mockReturnValue('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0')
    await wrapper.setProps({value: 'meta'})
    expect(wrapper.text()).toBe('⌘')
  })

  it('should convert the "meta" keyword to "Ctrl" on Linux', async () => {
    userAgentGetter.mockReturnValue('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36')
    await wrapper.setProps({value: 'meta'})
    expect(wrapper.text()).toBe('Ctrl')
  })

  it('should convert the "meta" keyword to "Ctrl" on Windows', async () => {
    userAgentGetter.mockReturnValue('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3')
    await wrapper.setProps({value: 'meta'})
    expect(wrapper.text()).toBe('Ctrl')
  })

  it('should hide the badge when no keys', async () => {
    await wrapper.setProps({value: []})
    expect(wrapper.isVisible()).toBeFalsy()
    await wrapper.setProps({value: ['l']})
    expect(wrapper.isVisible()).toBeTruthy()
  })
})
