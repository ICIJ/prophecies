import { createLocalVue, mount } from '@vue/test-utils'

import vShortkey from '@/directives/shortkey'

describe('vShortkey', () => {
  describe('a component with an array of shortkey', () => {
    const data = () => ({ calls: 0 })
    const methods = {
      callback() {
        this.calls++
      }
    }
    const template = '<div v-shortkey="[shortkey]" @shortkey="callback"></div>'
    const Component = { methods, template, props: ['shortkey'], data }
    const localVue = createLocalVue()
    localVue.directive('shortkey', vShortkey)

    describe('one wrapper with a single key shortcut', () => {
      let wrapper

      beforeEach(() => {
        wrapper = mount(Component, { localVue, propsData: { shortkey: 'a' } })
      })

      it('should call the `callback` function when pressing "a"', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(1)
      })

      it('should not call the `callback` function when pressing "b"', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 66 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(0)
      })

      it('should call the `callback` twice function when pressing "a" twice', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(2)
      })

      it('should not call the `callback` function when pressing "a" after the component is destroyed', async () => {
        await wrapper.destroy()
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(0)
      })

      it('should update the shortkey to "b" and not call the callback when pressing "a"', async () => {
        await wrapper.setProps({ shortkey: 'b' })
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(0)
      })

      it('should update the shortkey to "b" and call the callback when pressing "b"', async () => {
        await wrapper.setProps({ shortkey: 'b' })
        const event = new window.KeyboardEvent('keydown', { keyCode: 66 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(1)
      })

      it('should deactivate the shortkey to "a" and activate it again', async () => {
        await wrapper.setProps({ shortkey: '' })
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(0)
        await wrapper.setProps({ shortkey: 'a' })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(1)
      })
    })

    describe('two wrappers with the same key shortcut', () => {
      let wrapperBar
      let wrapperFoo

      beforeEach(() => {
        wrapperBar = mount(Component, { localVue, propsData: { shortkey: 'b' } })
        wrapperFoo = mount(Component, { localVue, propsData: { shortkey: ['b'] } })
      })

      it('should call the `callback` function when pressing "b"', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 66 })
        document.dispatchEvent(event)
        expect(wrapperBar.vm.calls).toBe(1)
        expect(wrapperFoo.vm.calls).toBe(1)
      })

      it('should call the `callback` function only with `wrapperFoo` if `wrapperBar` is destroyed', async () => {
        wrapperBar.destroy()
        const event = new window.KeyboardEvent('keydown', { keyCode: 66 })
        document.dispatchEvent(event)
        expect(wrapperBar.vm.calls).toBe(0)
        expect(wrapperFoo.vm.calls).toBe(1)
      })
    })
  })

  describe('a component with an object of shortkey', () => {
    const data = () => ({ calls: [] })
    const methods = {
      callback(e) {
        this.calls.push(e)
      }
    }
    const template = '<div v-shortkey="{ foo: \'a\', bar: \'b\' }" @shortkey="callback"></div>'
    const Component = { methods, template, data }
    const localVue = createLocalVue()
    localVue.directive('shortkey', vShortkey)

    describe('one wrapper with two single key shortcuts', () => {
      let wrapper

      beforeEach(() => {
        wrapper = mount(Component, { localVue, propsData: { shortkey: 'a' } })
      })

      it('should call the `callback` function when pressing "a"', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls.length).toBe(1)
      })

      it('should call the `callback` function when pressing "b"', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 66 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls.length).toBe(1)
      })

      it('should not call the `callback` function when pressing "c"', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 67 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls.length).toBe(0)
      })

      it('should pass the correct `srcKey` to `callback` function when pressing "a"', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls[0].detail).toEqual(expect.objectContaining({ srcKey: 'foo' }))
      })

      it('should pass the correct `srcKey` to `callback` function when pressing "b"', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 66 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls[0].detail).toEqual(expect.objectContaining({ srcKey: 'bar' }))
      })
    })
  })
})
