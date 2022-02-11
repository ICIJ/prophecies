import '@/store'
import { orderTasks, orderByProjectThenTask } from '@/utils/sort'
import Tip from '@/models/Tip'
import Task from '@/models/Task'

describe('utils/sort', () => {
  beforeAll(async () => {
    await Tip.api().get()
    await Task.api().get()
  })

  afterAll(() => {
    Tip.deleteAll()
    Task.deleteAll()
  })

  describe('orderByProjectThenTask', () => {
    beforeAll(async () => {
      await Tip.api().get()
    })

    afterAll(() => {
      Tip.deleteAll()
    })
    it('shouldn\'t sort when project and task aren\'t available', () => {
      const list = Tip.all()
      const sorted = orderByProjectThenTask(list)
      expect(list).toEqual(sorted)
    })
    it('should sort elements by project', () => {
      const tips = Tip.query().with('project').get()
      const sorted = orderByProjectThenTask(tips)

      expect(sorted[0].project).toBeNull()
      expect(sorted[1].project.name).toBe('Aladdin')
      expect(sorted[2].project.name).toBe('Aladdin')
      expect(sorted[3].project.name).toBe('Aladdin')
      expect(sorted[4].project.name).toBe('Chronos')
      expect(sorted[5].project.name).toBe('Chronos')
      expect(sorted[6].project.name).toBe('Demeter')
    })

    it('should sort elements project then by task if available', () => {
      const tips = Tip.query().with('project').with('task').get()
      const sorted = orderByProjectThenTask(tips)
      expect(sorted[1].project.name).toBe('Aladdin')
      expect(sorted[1].task.name).toBe('Addresses')
      expect(sorted[2].project.name).toBe('Aladdin')
      expect(sorted[2].task.name).toBe('Another Task')

      expect(sorted[4].project.name).toBe('Chronos')
      expect(sorted[4].task).toBeNull()
      expect(sorted[4].project.name).toBe('Chronos')
      expect(sorted[5].task.name).toBe('Shops')
    })
  })
  describe('sort tasks ', () => {
    beforeAll(async () => {
      await Task.api().get()
    })

    afterAll(() => {
      Task.deleteAll()
    })
    it('from open to close', () => {
      const sorted = orderTasks(Task.all())
      expect(sorted).toHaveLength(5)

      let task = sorted[0]
      expect(task.status).toEqual('LOCKED')
      expect(task.name).toEqual('Addresses')
      task = sorted[1]
      expect(task.status).toEqual('OPEN')
      expect(task.name).toEqual('Cats')
      task = sorted[2]
      expect(task.status).toEqual('OPEN')
      expect(task.name).toEqual('Phones')
      task = sorted[3]
      expect(task.status).toEqual('OPEN')
      expect(task.name).toEqual('Shops')
      task = sorted[4]
      expect(task.status).toEqual('CLOSED')
      expect(task.name).toEqual('Immatriculations')
    })
  })
})
