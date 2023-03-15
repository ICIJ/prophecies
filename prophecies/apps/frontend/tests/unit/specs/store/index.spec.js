import { createStore, default as defaultStore } from '@/store'

describe('store', () => {
  describe('default', () => {
    it('should instantiate an object', () => {
      expect(defaultStore).toBeInstanceOf(Object)
    })

    it('shouldn\'t be in strict mode', () => {
      expect(defaultStore.strict).toBeFalsy()
    })

    it('should define an `app` module', () => {
      expect(defaultStore.state.app).toBeDefined()
    })
  })

  describe('created store', () => {
    let store

    beforeAll(() => {
      store = createStore()
    })

    it('should instantiate an object', () => {
      expect(store).toBeInstanceOf(Object)
    })

    it('shouldn\'t be in strict mode', () => {
      expect(store.strict).toBeFalsy()
    })

    it('should define an `app` module', () => {
      expect(store.state.app).toBeDefined()
    })

    it('should create a new instance of the store', () => {
      const otherStore = createStore()
      expect(store).not.toBe(otherStore)
    })
  })
})
