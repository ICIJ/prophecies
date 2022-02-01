import '@/store'
import TaskUserChoiceStatistics from '@/models/TaskUserChoiceStatistics'

describe('TaskUserChoiceStatistics', () => {
  beforeAll(async () => {
    await TaskUserChoiceStatistics.api().get()
  })

  afterAll(() => {
    TaskUserChoiceStatistics.deleteAll()
  })

  it('should retrieve 9 user choice stats', () => {
    expect(TaskUserChoiceStatistics.all()).toHaveLength(9)
  })

  it('should have one user object as checker', () => {
    const { checker } = TaskUserChoiceStatistics.query().with('checker').find('12')
    expect(checker.id).toBe('1')
    expect(checker.username).toBe('olivia')
  })
  it('should have one task object', () => {
    const { task } = TaskUserChoiceStatistics.query().with('task').find('12')
    expect(task.id).toBe('3')
  })
  it('should have one choice object', () => {
    const { choice } = TaskUserChoiceStatistics.query().with('choice').find('12')
    expect(choice.id).toBe('1')
  })

  it('should have an accessor the round and the count by choice', () => {
    const { round, count } = TaskUserChoiceStatistics.query().find('12')
    expect(round).toBe(1)
    expect(count).toBe(39)
  })
})
