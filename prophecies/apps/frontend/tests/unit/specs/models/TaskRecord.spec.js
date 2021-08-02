import '@/store'
import TaskRecord from '@/models/TaskRecord'

describe('TaskRecord', () => {
  it('should returns a list of task record', async () => {
    await TaskRecord.api().get()
    expect(TaskRecord.all()).toHaveLength(2)
    expect(TaskRecord.find(1).url).toBe('http://localhost/api/v1/task-records/1/')
    expect(TaskRecord.find(3).url).toBe('http://localhost/api/v1/task-records/3/')
  })

  it('should returns a nested of task', async () => {
    await TaskRecord.api().get()
    expect(TaskRecord.query().with('task').find(1).task.id).toBe(1)
    expect(TaskRecord.query().with('task').find(3).task.id).toBe(1)
  })

  it('should returns an original_value', async () => {
    await TaskRecord.api().get()
    expect(TaskRecord.find(1).original_value).toBe('fronce')
    expect(TaskRecord.find(3).original_value).toBe('La France')
  })
})
