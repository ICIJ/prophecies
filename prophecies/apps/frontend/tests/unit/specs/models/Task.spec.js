import '@/store'
import Task from '@/models/Task'

describe('Task', () => {
  beforeAll(async () => {
    await Task.api().get()
  })

  afterAll(() => {
    Task.deleteAll()
  })

  it('should return a list of task record', () => {
    expect(Task.all()).toHaveLength(2)
  })

  it('should return a name and a description', () => {
    expect(Task.find(1).name).toBe('Addresses')
    expect(Task.find(1).description).toBe('A collection of adresses to fact check.')
  })

  it('should not return a nested choice_group if not requested explicitely', () => {
    expect(Task.find(1).choice_group).toBeNull()
  })

  it('should return a choice_group if requested explicitely', () => {
    const task = Task.query().with('choice_group').find(2)
    expect(task.choice_group).not.toBeNull()
    expect(task.choice_group.id).toBe('1')
    expect(task.choice_group.name).toBe('Is it correct?')
  })
})
