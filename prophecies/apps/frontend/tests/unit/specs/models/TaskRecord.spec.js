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
    expect(TaskRecord.find(1)).not.toBeNull()
    expect(TaskRecord.find(3)).not.toBeNull()
  })

  it('should return a nested of task', async () => {
    expect(TaskRecord.query().with('task').find(1).task.name).toBe('Addresses')
    expect(TaskRecord.query().with('task').find(3).task.name).toBe('Addresses')
  })

  it('should return an originalValue', async () => {
    expect(TaskRecord.find(1).originalValue).toBe('fronce')
    expect(TaskRecord.find(3).originalValue).toBe('La France')
  })

  it('should return a saved attribute', async () => {
    expect(TaskRecord.find(1).bookmarked).toBeFalsy()
    expect(TaskRecord.find(3).bookmarked).toBeTruthy()
  })
})
