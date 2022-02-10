import '@/store'
import { sortByProjectThenTask } from '@/utils/sort'
import Tip from '@/models/Tip'

describe('utils/sort', () => {
  beforeAll(async () => {
    await Tip.api().get()
  })

  afterAll(() => {
    Tip.deleteAll()
  })

  describe('sortByProjectThenTask', () => {
    it('shouldn\'t sort when project and task aren\'t available', () => {
      var list = Tip.all()
      var sorted = list.sort(sortByProjectThenTask)
      expect(list).toBe(sorted)
    })
    it('should sort elements by project', () => {
      var sorted = Tip.query().with('project').get().sort(sortByProjectThenTask)
      expect(sorted[0].project).toBeNull()
      expect(sorted[1].project.name).toBe('Aladdin')
      expect(sorted[2].project.name).toBe('Aladdin')
      expect(sorted[3].project.name).toBe('Aladdin')
      expect(sorted[4].project.name).toBe('Chronos')
      expect(sorted[5].project.name).toBe('Chronos')
      expect(sorted[6].project.name).toBe('Demeter')
    })

    it('should sort elements project then by task if available', () => {
      var sorted = Tip.query().with('project').with('task').get().sort(sortByProjectThenTask)
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
})
