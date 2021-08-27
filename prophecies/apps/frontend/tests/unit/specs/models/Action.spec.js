import '@/store'
import Action from '@/models/Action'

describe('Action', () => {
  describe('get actions relayed to a task record', () => {
    beforeAll(async () => {
      await Action.api().forTaskRecord(3)
    })

    afterAll(() => {
      Action.deleteAll()
    })

    it('should have created one action', async () => {
      expect(Action.all()).toHaveLength(1)
      expect(Action.find(13).verb).toBe('reviewed')
    })
  })
})
