import '@/store'
import Task from '@/models/Task'

describe('Task', () => {
  beforeAll(async () => {
    await Task.api().get()
  })

  afterAll(() => {
    Task.deleteAll()
  })

  it('should returns a list of task record', () => {
    expect(Task.all()).toHaveLength(1)
    expect(Task.find(1).url).toBe('http://localhost/api/v1/tasks/1/')
  })

  it('should return a name and a description', () => {
    expect(Task.find(1).name).toBe('Addresses')
    expect(Task.find(1).description).toBe('A collection of adresses to fact check.')
  })

  it('should not return a nested choice_group if not requested explicitely', () => {
    expect(Task.find(1).choice_group).toBeNull()
  })

  it('should return a choice_group if requested explicitely', () => {
    const task = Task.query().with('choice_group').find(1)
    expect(task.choice_group).not.toBeNull()
    expect(task.choice_group.id).toBe(1)
    expect(task.choice_group.name).toBe('Is it correct?')
  })

  it('should not return nested choices if not requested explicitely', () => {
    const task = Task.query().with('choice_group').find(1)
    expect(task.choice_group.choices).toHaveLength(0)
  })

  it('should return nested choices if requested explicitely', () => {
    const task = Task.query().with('choice_group').with('choice_group.choices').find(1)
    expect(task.choice_group.choices).toHaveLength(3)
    expect(task.choice_group.choices[0].value).toBe('correct')
  })
})
