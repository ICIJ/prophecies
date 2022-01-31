import '@/store'
// import User from '@/models/User'
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
})
