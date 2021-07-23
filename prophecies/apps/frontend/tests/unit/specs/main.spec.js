import Vue from 'vue'
import { createLocalVue } from '@vue/test-utils'

import { Core, createCore } from '@/core'

describe('main', () => {
  const { localVue } = createLocalVue()
  let core = null
  let vm = null

  beforeEach(async () => {
    const app = document.createElement('div')
    app.setAttribute('id', 'app')
    document.body.appendChild(app)
    // Mock Core methods that use the backend
    jest.spyOn(Core.prototype, 'getUser').mockResolvedValue({ username: 'foo' })
    jest.spyOn(Core.prototype, 'getSettings').mockResolvedValue({ })
    // Create a core instance
    core = createCore(localVue)
    vm = await core.ready
    vm = vm.mount()
  })

  afterAll(() => {
    jest.restoreAllMocks()
  })

  it('should instantiate Vue', () => {
    expect(vm).toBeInstanceOf(Vue)
    expect(vm.$router).toBeDefined()
    expect(vm.$store).toBeDefined()
  })
})
