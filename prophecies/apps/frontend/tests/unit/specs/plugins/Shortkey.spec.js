import { createLocalVue, mount } from '@vue/test-utils'
import Shortkey from '@/plugins/Shortkey'

describe('Shortkey', () => {
  describe('a component with one shortkey', () => {
    const data = () => ({ calls: 0 })
    const template = `<div></div>`
    const Component = { template, data }
    const localVue = createLocalVue()
    localVue.use(Shortkey)

    describe('one wrapper with a single key shortcut', () => {
      let wrapper

      beforeEach(() => {
        wrapper = mount(Component, { localVue })
        wrapper.vm.$shortkey.bind('a', () => wrapper.vm.calls++)
      })

      afterEach(async () => {
        await wrapper.destroy()
      })

      it('should call the callback function when pressing "a"', () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(1)
      })

      it('should not call the callback function when pressing "b"', async () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 66 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(0)
      })

      it('should call the callback twice function when pressing "a" twice', () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(2)
      })

      it('should not call the callback function when pressing "a" after the component is destroyed', async () => {
        await wrapper.destroy()
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(0)
      })

      it('should bind two different callbacks to the same component', () => {
        wrapper.vm.$shortkey.bind('b', () => wrapper.vm.calls++)
        wrapper.vm.$shortkey.bind('b', () => wrapper.vm.calls++)
        const event = new window.KeyboardEvent('keydown', { keyCode: 66 })
        document.dispatchEvent(event)
        expect(wrapper.vm.calls).toBe(1)
      })
    })

    describe('two wrappers with the same shortkey', () => {
      let wrapperBar
      let wrapperFoo

      beforeEach(() => {
        wrapperBar = mount(Component, { localVue })
        wrapperBar.vm.$shortkey.bind('a', () => wrapperBar.vm.calls++)
        wrapperFoo = mount(Component, { localVue })
        wrapperFoo.vm.$shortkey.bind('a', () => wrapperFoo.vm.calls++)
      })

      afterEach(async () => {
        await wrapperBar.destroy()
        await wrapperFoo.destroy()
      })

      it('should call the two callback functions when pressing "a"', () => {
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapperBar.vm.calls).toBe(1)
        expect(wrapperFoo.vm.calls).toBe(1)
      })

      it('should call only one callback function when pressing a component is destroyed', async () => {
        await wrapperBar.destroy()
        const event = new window.KeyboardEvent('keydown', { keyCode: 65 })
        document.dispatchEvent(event)
        expect(wrapperBar.vm.calls).toBe(0)
        expect(wrapperFoo.vm.calls).toBe(1)
      })      
      
      it('should call only one callback function for the current scope', async () => {
        wrapperBar.vm.$shortkey.bind('b', 'bar', () => wrapperBar.vm.calls++)
        wrapperFoo.vm.$shortkey.bind('b', 'foo', () => wrapperFoo.vm.calls++)
        // Set the current scope to "bar" (instead of "all")
        wrapperFoo.vm.$shortkey.setScope('bar')
        const event = new window.KeyboardEvent('keydown', { keyCode: 66 })
        document.dispatchEvent(event)
        expect(wrapperBar.vm.calls).toBe(1)
        expect(wrapperFoo.vm.calls).toBe(0)
      })     
      
      it('should call only one callback function if the other is deactivated', async () => {
        wrapperBar.vm.$shortkey.bind('c', 'bar', () => wrapperBar.vm.calls++)
        wrapperFoo.vm.$shortkey.bind('c', 'foo', () => wrapperFoo.vm.calls++)
        wrapperFoo.vm.$shortkey.deactivate()
        const event = new window.KeyboardEvent('keydown', { keyCode: 67 })
        document.dispatchEvent(event)
        expect(wrapperBar.vm.calls).toBe(1)
        expect(wrapperFoo.vm.calls).toBe(0)
      })
    })
  })
})