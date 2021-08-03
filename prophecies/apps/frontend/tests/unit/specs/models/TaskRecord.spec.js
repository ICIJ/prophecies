import '@/store'
import TaskRecord from '@/models/TaskRecord'

describe('TaskRecord', () => {
  beforeAll(async () => {
    await TaskRecord.api().get()
  })

  afterAll(() => {
    TaskRecord.deleteAll()
  })

  it('should return a list of task record', async () => {
    expect(TaskRecord.all()).toHaveLength(2)
    expect(TaskRecord.find(1)).not.toBeNull()
    expect(TaskRecord.find(3)).not.toBeNull()
  })

  it('should return a nested of task', async () => {
    expect(TaskRecord.query().with('task').find(1).task.id).toBe(1)
    expect(TaskRecord.query().with('task').find(3).task.id).toBe(1)
  })

  it('should return an original_value', async () => {
    expect(TaskRecord.find(1).original_value).toBe('fronce')
    expect(TaskRecord.find(3).original_value).toBe('La France')
  })
})
