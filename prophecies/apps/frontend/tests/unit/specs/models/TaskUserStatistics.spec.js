import '@/store'
import TaskUserStatistics from '@/models/TaskUserStatistics'

describe('TaskUserStatistics', () => {
  beforeAll(async () => {
    await TaskUserStatistics.api().get()
  })

  afterAll(() => {
    TaskUserStatistics.deleteAll()
  })

  it('should retrieve 7 user stats', () => {
    expect(TaskUserStatistics.all()).toHaveLength(7)
  })

  it('should have one user object as checker', () => {
    const { checker } = TaskUserStatistics.query().with('checker').find('2')
    expect(checker.id).toBe('1')
    expect(checker.username).toBe('olivia')
  })
  it('should have one task object', () => {
    const { task } = TaskUserStatistics.query().with('task').find('2')
    expect(task.id).toBe('1')
  })

  it('should have an accessor for counting done, pending, total reviews and progress', () => {
    const { doneCount, pendingCount, totalCount, progress } = TaskUserStatistics.query().with('task').find('2')
    expect(doneCount).toBe(12)
    expect(pendingCount).toBe(187)
    expect(totalCount).toBe(199)
    expect(progress).toBe(6.030150753768844)
  })
})
