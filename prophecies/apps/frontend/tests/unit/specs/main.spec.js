import Vue from 'vue'
import { createLocalVue } from '@vue/test-utils'

import { createCore } from '@/core'

jest.mock('axios', () => {
  return {
    get: jest.fn().mockResolvedValue({ data: { } })
  }
})

describe('main', () => {
  const { localVue } = createLocalVue()
  let core = null
  let vm = null

  beforeEach(async () => {
    const app = document.createElement('div')
    app.setAttribute('id', 'app')
    document.body.appendChild(app)
    core = createCore(localVue)
    vm = await core.ready
    vm = vm.mount()
  })

  it('should instantiate Vue', () => {
    expect(vm).toBeInstanceOf(Vue)
    expect(vm.$router).toBeDefined()
    expect(vm.$store).toBeDefined()
  })
})
